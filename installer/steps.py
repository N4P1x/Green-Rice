"""Install steps: packages → fonts → build → link → apps → verify.

Each step is a function `step(ctx) -> (ok, message)` and is skipped if already
done in InstallState (idempotent) or if the user deselected it.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Callable

from .backup import BackupManager
from .detector import SystemInfo
from .packages import ARCH_PACKAGES, PackageManager
from .state import InstallState
from .ui import err, info, ok, warn

REPO = Path(__file__).resolve().parent.parent  # Green-Rice root
HOME = Path.home()
CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))
LOCAL_BIN = HOME / ".local" / "bin"

# Components that map 1:1 to install.sh manifest entries (built by build.sh)
COMPONENT_SETS = [
    "packages",
    "fonts",
    "dotfiles",
    "hypr-lua",
    "firefox",
    "obsidian",
    "vscode",
    "vencord",
    "steam",
    "wallpapers",
    "scripts",
    "verify",
]


def _run(cmd: list[str], dry: bool = False) -> tuple[bool, str]:
    if dry:
        return True, "[dry] " + " ".join(cmd)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return proc.returncode == 0, (proc.stderr or proc.stdout or "").strip()
    except subprocess.TimeoutExpired:
        return False, "timed out"
    except FileNotFoundError:
        return False, "command not found"
    except Exception as exc:
        return False, str(exc)


def _which(cmd: str) -> str | None:
    return shutil.which(cmd)


class InstallContext:
    def __init__(
        self,
        info: SystemInfo,
        pm: PackageManager,
        state: InstallState,
        backup: BackupManager,
        dry: bool = False,
        selected: list[str] | None = None,
    ):
        self.info = info
        self.pm = pm
        self.state = state
        self.backup = backup
        self.dry = dry
        self.selected = set(selected or [])


# ---------------------------------------------------------------- steps ---


def step_packages(ctx: InstallContext) -> tuple[bool, str]:
    if "packages" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("packages"):
        return True, "already done"
    pm = ctx.pm
    normal = []
    aur = []
    for ps in ARCH_PACKAGES:
        if ps.aur:
            aur.extend(ps.pkgs)
        else:
            normal.extend(ps.pkgs)
    missing = pm.missing(normal)
    if missing:
        ok_run, out = pm.install(missing, dry=ctx.dry)
        if not ok_run:
            warn(f"pacman install had issues: {out}")
    # best-effort: try to satisfy missing even if pacman said no
    if aur:
        helper = pm.aur_helper()
        if helper:
            ok_run, out = pm.install_aur(
                [p for p in aur if p not in pm.missing([])], dry=ctx.dry
            )
            if not ok_run:
                warn(f"AUR install ({helper}) had issues: {out}")
        else:
            warn("AUR packages need yay/paru — install hyprlang2lua manually")
    ctx.state.mark("packages", f"mgr={pm.mgr}")
    return True, f"packages via {pm.mgr}"


def step_fonts(ctx: InstallContext) -> tuple[bool, str]:
    if "fonts" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("fonts"):
        return True, "already done"
    # skip if fonts already present
    if ctx.info.fonts:
        ctx.state.mark("fonts", "already present")
        return True, "fonts already installed"
    if ctx.dry:
        ctx.state.mark("fonts", "dry-run")
        return True, "would download fonts"
    fdir = HOME / ".local" / "share" / "fonts" / "JetBrainsMonoNerd"
    fdir.mkdir(parents=True, exist_ok=True)
    import urllib.request

    try:
        zip_path = Path("/tmp/JBM.zip")
        urllib.request.urlretrieve(
            "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.zip",
            zip_path,
        )
        _run(
            [
                "unzip",
                "-o",
                "-j",
                str(zip_path),
                "JetBrainsMonoNerdFontMono-Regular.ttf",
                "JetBrainsMonoNerdFontMono-Bold.ttf",
                "JetBrainsMonoNerdFontMono-Italic.ttf",
                "JetBrainsMonoNerdFontMono-Medium.ttf",
                "JetBrainsMonoNerdFont-Regular.ttf",
                "JetBrainsMonoNerdFont-Bold.ttf",
                "-d",
                str(fdir),
            ]
        )
        urllib.request.urlretrieve(
            "https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoColorEmoji.ttf",
            HOME / ".local" / "share" / "fonts" / "NotoColorEmoji.ttf",
        )
        _run(["fc-cache", "-f", str(HOME / ".local" / "share" / "fonts")])
        zip_path.unlink(missing_ok=True)
        ctx.state.mark("fonts", "downloaded to ~/.local/share/fonts")
        return True, "fonts installed (user-local, no sudo)"
    except Exception as exc:
        return False, f"font download failed: {exc}"


def step_dotfiles(ctx: InstallContext) -> tuple[bool, str]:
    if "dotfiles" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("dotfiles"):
        return True, "already done"
    # back up existing ~/.config targets before overwriting
    targets = [
        CONFIG / "hypr",
        CONFIG / "kitty",
        CONFIG / "waybar",
        CONFIG / "wofi",
        CONFIG / "mako",
        CONFIG / "gtk-3.0",
        CONFIG / "gtk-4.0",
        CONFIG / "btop",
        CONFIG / "cava",
        HOME / ".kdeglobals",
    ]
    targets = [t for t in targets if t.exists()]
    if targets:
        ctx.backup.snapshot("pre-install", targets)
    # build + install using the repo's own scripts
    build = REPO / "build.sh"
    install = REPO / "install.sh"
    if not build.exists() or not install.exists():
        return False, "build.sh / install.sh missing from repo"
    ok_run, out = _run(["bash", str(build), "all"], dry=ctx.dry)
    if not ok_run:
        return False, f"build.sh failed: {out}"
    mode = "copy" if not _which("ln") else "link"
    ok_run, out = _run(["bash", str(install), mode], dry=ctx.dry)
    if not ok_run:
        return False, f"install.sh failed: {out}"
    ctx.state.mark("dotfiles", f"mode={mode}")
    return True, f"dotfiles built + {mode}ed into ~/.config"


def step_hypr_lua(ctx: InstallContext) -> tuple[bool, str]:
    if "hypr-lua" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("hypr-lua"):
        return True, "already done"
    sync = REPO / "scripts" / "sync-hypr-lua.sh"
    if sync.exists() and _which("bash"):
        ok_run, out = _run(["bash", str(sync)], dry=ctx.dry)
        if not ok_run:
            warn(f"sync-hypr-lua: {out}")
    # append require("theme") if missing
    lua = CONFIG / "hypr" / "hyprland.lua"
    if lua.exists():
        text = lua.read_text(encoding="utf-8", errors="replace")
        if 'require("theme")' not in text and not ctx.dry:
            lua.write_text(text + '\nrequire("theme")\n', encoding="utf-8")
            info('appended require("theme") to hyprland.lua')
    ctx.state.mark("hypr-lua", "theme synced")
    return True, "hyprland.lua theme synced"


def _app_config(
    ctx: InstallContext,
    name: str,
    src: Path,
    dst_dir: Path,
    dst_file: str,
    backup_label: str,
) -> tuple[bool, str]:
    """Generic: back up existing, copy a generated app config into place."""
    if not src.exists():
        return False, f"{src} not built (run build.sh first)"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / dst_file
    if dst.exists():
        ctx.backup.snapshot(backup_label, [dst])
    if ctx.dry:
        return True, f"would copy {src} -> {dst}"
    shutil.copy2(src, dst)
    return True, f"{name} config installed"


def step_firefox(ctx: InstallContext) -> tuple[bool, str]:
    if "firefox" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("firefox"):
        return True, "already done"
    # find firefox profile
    prof = None
    for base in (
        HOME / ".mozilla" / "firefox",
        HOME / ".config" / "mozilla" / "firefox",
    ):
        ini = base / "profiles.ini"
        if ini.exists():
            for line in ini.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("Path="):
                    cand = base / line.split("=", 1)[1]
                    if cand.is_dir():
                        prof = cand
                        break
                if prof:
                    break
        if prof:
            break
    if not prof:
        warn("no Firefox profile — skipping (launch Firefox once, then re-run)")
        ctx.state.mark("firefox", "no profile")
        return True, "no Firefox profile found"
    src = REPO / "dist" / "firefox" / "userChrome.css"
    ok_run, msg = _app_config(
        ctx, "firefox", src, prof / "chrome", "userChrome.css", "firefox"
    )
    if ok_run and not ctx.dry:
        # enable userChrome in user.js
        ujs = prof / "user.js"
        extra = (
            'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);\n'
            'user_pref("ui.systemUsesDarkTheme", true);\n'
        )
        cur = ujs.read_text(encoding="utf-8", errors="replace") if ujs.exists() else ""
        if "legacyUserProfileCustomizations.stylesheets" not in cur:
            ujs.write_text(cur + extra, encoding="utf-8")
    return ok_run, msg


def step_obsidian(ctx: InstallContext) -> tuple[bool, str]:
    if "obsidian" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("obsidian"):
        return True, "already done"
    vault = None
    cand = HOME / "Mind" / "MIND"
    if cand.is_dir() and (cand / ".obsidian").is_dir():
        vault = cand
    else:
        for d in HOME.glob("*/.obsidian"):
            if d.is_dir():
                vault = d.parent
                break
    if not vault:
        warn("no Obsidian vault found — pass --vault PATH or create ~/Mind/MIND")
        ctx.state.mark("obsidian", "no vault")
        return True, "no Obsidian vault"
    src = REPO / "dist" / "obsidian" / "miasma.css"
    ok_run, msg = _app_config(
        ctx, "obsidian", src, vault / ".obsidian" / "snippets", "miasma.css", "obsidian"
    )
    if ok_run and not ctx.dry:
        try:
            import json

            ap = vault / ".obsidian" / "appearance.json"
            data = json.loads(ap.read_text(encoding="utf-8")) if ap.exists() else {}
            snips = sorted(set(data.get("enabledCssSnippets", [])) | {"miasma"})
            data["enabledCssSnippets"] = snips
            ap.write_text(json.dumps(data, indent=2), encoding="utf-8")
            info("enabled 'miasma' snippet in Obsidian appearance.json")
        except Exception as exc:
            warn(f"couldn't enable snippet: {exc}")
    return ok_run, msg


def step_vscode(ctx: InstallContext) -> tuple[bool, str]:
    if "vscode" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("vscode"):
        return True, "already done"
    src = REPO / "dist" / "vscode" / "themes" / "miasma-color-theme.json"
    if not src.exists():
        warn("VS Code theme not built — skipping")
        ctx.state.mark("vscode", "not built")
        return True, "theme not built"
    # VS Code OSS extensions dir (this machine uses .vscode-oss)
    ext_dir = (
        HOME / ".vscode-oss" / "extensions" / "local.miasma-theme-0.1.0" / "themes"
    )
    ok_run, msg = _app_config(
        ctx, "vscode", src, ext_dir, "miasma-color-theme.json", "vscode"
    )
    return ok_run, msg


def step_vencord(ctx: InstallContext) -> tuple[bool, str]:
    if "vencord" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("vencord"):
        return True, "already done"
    src = REPO / "dist" / "vencord" / "miasma.theme.css"
    if not src.exists():
        warn("Vencord theme not built — skipping")
        ctx.state.mark("vencord", "not built")
        return True, "theme not built"
    info("Vencord theme built at dist/vencord/miasma.theme.css")
    info("Load it in Vencord → Themes, or paste as a custom theme")
    ctx.state.mark("vencord", "built")
    return True, "vencord theme ready (load manually in Vencord)"


def step_steam(ctx: InstallContext) -> tuple[bool, str]:
    if "steam" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("steam"):
        return True, "already done"
    src = REPO / "dist" / "steam" / "steam.css"
    if not src.exists():
        warn("Steam theme not built — skipping")
        ctx.state.mark("steam", "not built")
        return True, "theme not built"
    info("Steam theme built at dist/steam/steam.css")
    info("Point Steam → Settings → Customize → Adwaita at this file")
    ctx.state.mark("steam", "built")
    return True, "steam theme ready (apply manually in Steam)"


def step_wallpapers(ctx: InstallContext) -> tuple[bool, str]:
    if "wallpapers" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("wallpapers"):
        return True, "already done"
    wall = REPO / "wallpapers"
    dest = HOME / ".local" / "share" / "wallpapers" / "green-rice"
    if not ctx.dry:
        if dest.exists():
            ctx.backup.snapshot("wallpapers", [dest])
        shutil.copytree(wall, dest, dirs_exist_ok=True)
    ctx.state.mark("wallpapers", f"copied to {dest}")
    return True, f"wallpapers copied to {dest}"


def step_scripts(ctx: InstallContext) -> tuple[bool, str]:
    if "scripts" not in ctx.selected:
        return True, "skipped (not selected)"
    if ctx.state.is_done("scripts"):
        return True, "already done"
    LOCAL_BIN.mkdir(parents=True, exist_ok=True)
    for script in ("power-menu", "bg-menu", "audio-menu", "smart-kill"):
        src = REPO / "scripts" / script
        dst = LOCAL_BIN / script
        if dst.exists() or dst.is_symlink():
            ctx.backup.snapshot("scripts", [dst])
        if not ctx.dry and src.exists():
            if dst.is_symlink() or dst.exists():
                dst.unlink()
            os.symlink(src, dst)
            os.chmod(dst, 0o755)
    ctx.state.mark("scripts", f"linked into {LOCAL_BIN}")
    return True, f"scripts linked into {LOCAL_BIN}"


def step_verify(ctx: InstallContext) -> tuple[bool, str]:
    if "verify" not in ctx.selected:
        return True, "skipped (not selected)"
    checks = [
        ("hyprland", "hyprland"),
        ("kitty", "kitty"),
        ("waybar", "waybar"),
        ("wofi", "wofi"),
        ("mako", "mako"),
        ("hyprland.conf", str(CONFIG / "hypr" / "hyprland.conf")),
        ("kitty theme", str(CONFIG / "kitty" / "themes" / "miasma.conf")),
        ("waybar style", str(CONFIG / "waybar" / "style.css")),
        ("font JetBrainsMono NF", "JetBrainsMono Nerd Font Mono"),
        ("font Noto Color Emoji", "Noto Color Emoji"),
    ]
    results = []
    for label, target in checks:
        if target.startswith("/") or target == target:  # path check
            results.append(("file", label, check_file(target)[1]))
        else:
            results.append(("cmd", label, check_command(label, target)[1]))
    # flatten for display
    rows = [(label, result) for _, label, result in results]
    fails = [r for r in rows if r[1].startswith("FAIL")]
    ctx.state.mark("verify", f"{len(rows) - len(fails)}/{len(rows)} passed")
    return (len(fails) == 0), f"{len(rows) - len(fails)}/{len(rows)} checks passed"


STEP_REGISTRY: dict[str, Callable[[InstallContext], tuple[bool, str]]] = {
    "packages": step_packages,
    "fonts": step_fonts,
    "dotfiles": step_dotfiles,
    "hypr-lua": step_hypr_lua,
    "firefox": step_firefox,
    "obsidian": step_obsidian,
    "vscode": step_vscode,
    "vencord": step_vencord,
    "steam": step_steam,
    "wallpapers": step_wallpapers,
    "scripts": step_scripts,
    "verify": step_verify,
}
