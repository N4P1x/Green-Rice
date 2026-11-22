"""Green-Rice installer entry point.

Run:  python3 -m green_rice_installer
      or ./installer/green-rice-install  (see installer/green-rice-install shim)
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import __prog__, __version__
from .backup import BackupManager
from .cli import build_parser, parse_args
from .detector import detect, render_info
from .packages import PackageManager
from .state import InstallState
from .steps import COMPONENT_SETS, STEP_REGISTRY, InstallContext
from .ui import (
    ComponentsMenu,
    banner,
    color_swatches,
    confirm,
    console,
    err,
    info,
    ok,
    prompt,
    section,
    summary_table,
    warn,
)


DEFAULT_SELECTED = list(COMPONENT_SETS)


def run_interactive(ctx: InstallContext, args) -> None:
    """The TUI: detect → preview theme → pick components → back up → install → verify."""
    banner()
    section("System detected")
    console.print(render_info(ctx.info))
    console.print()

    section("Miasma theme preview")
    console.print(color_swatches())
    console.print()

    # Pre-flight: what's missing
    section("Pre-flight check")
    missing_pm = []
    if ctx.info.package_manager == "none":
        missing_pm.append("no package manager detected (configs only)")
    if not ctx.info.sudo_passwordless and ctx.info.package_manager in (
        "pacman",
        "apt",
        "dnf",
    ):
        missing_pm.append("no passwordless sudo (packages must be installed manually)")
    if not ctx.info.hyprland_running:
        info(
            "Hyprland not currently running — configs still installed; log out/in to apply"
        )
    if missing_pm:
        for m in missing_pm:
            warn(m)
    console.print()

    # Component selection
    menu_items = [
        (
            "packages",
            "System packages",
            "packages" in ctx.selected and not args.skip_packages,
        ),
        (
            "fonts",
            "Fonts (Nerd + emoji)",
            "fonts" in ctx.selected and not args.skip_fonts,
        ),
        ("dotfiles", "Dotfiles (build + link)", True),
        ("hypr-lua", "Hyprland Lua theme", True),
        ("firefox", "Firefox userChrome + prefs", True),
        ("obsidian", "Obsidian miasma snippet", True),
        ("vscode", "VS Code theme", True),
        ("vencord", "Vencord Discord theme", True),
        ("steam", "Steam Adwaita CSS", True),
        ("wallpapers", "Miasma wallpapers", True),
        ("scripts", "power/bg/audio menus + smart-kill", True),
        ("verify", "Post-install verification", True),
    ]
    # honor --select / --skip flags
    if args.select:
        want = set(args.select)
        menu_items = [(k, l, k in want) for k, l, _ in menu_items]
    if args.skip_packages:
        menu_items = [(k, l, False if k == "packages" else s) for k, l, s in menu_items]
    if args.skip_fonts:
        menu_items = [(k, l, False if k == "fonts" else s) for k, l, s in menu_items]

    menu = ComponentsMenu(menu_items)
    chosen = menu.run()
    ctx.selected = set(chosen)

    if not ctx.selected:
        warn("Nothing selected — nothing to install.")
        return

    console.print()
    section("Smart backup before install")
    # back up anything that exists in ~/.config that we might touch
    from .steps import CONFIG, HOME

    pre_targets = [
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
    pre_targets = [t for t in pre_targets if t.exists()]
    if pre_targets and not args.dry_run:
        ctx.backup.snapshot("pre-install", pre_targets)
    elif not pre_targets:
        info("no existing configs to back up")

    if not args.yes:
        console.print()
        if not confirm(
            f"Install {len(ctx.selected)} selected components now?", default=True
        ):
            warn("Install cancelled.")
            return

    # ---- run the steps ----
    section("Installing")
    from .ui import progress_bar

    progress = progress_bar()
    with progress:
        total = len(ctx.selected)
        for idx, key in enumerate(ctx.selected, 1):
            task = progress.add_task(f"[{idx}/{total}] {key}", total=1)
            step = STEP_REGISTRY[key]
            try:
                success, message = step(ctx)
            except Exception as exc:  # never let one step kill the whole install
                success, message = False, f"step raised: {exc}"
            progress.update(task, completed=1)
            if success:
                ok(f"{key}: {message}")
            else:
                err(f"{key}: {message}")
    console.print()

    # ---- verify ----
    if "verify" in ctx.selected:
        section("Verification")
        from .verify import run_checks, check_command, check_file

        checks = [
            ("hyprland", check_command("hyprland", "hyprland")),
            ("kitty", check_command("kitty", "kitty")),
            ("waybar", check_command("waybar", "waybar")),
            ("wofi", check_command("wofi", "wofi")),
            ("mako", check_command("mako", "mako")),
            ("hyprland.conf", check_file(str(CONFIG / "hypr" / "hyprland.conf"))),
            (
                "kitty theme",
                check_file(str(CONFIG / "kitty" / "themes" / "miasma.conf")),
            ),
            ("waybar style", check_file(str(CONFIG / "waybar" / "style.css"))),
            (
                "font JetBrainsMono NF",
                check_command("fc-match JetBrainsMono Nerd Font Mono", "fc-match"),
            ),
            (
                "font Noto Color Emoji",
                check_command("fc-match Noto Color Emoji", "fc-match"),
            ),
        ]
        # run_checks expects (label, result) — build that
        rows = [(label, result) for label, (_, result) in checks]
        console.print(summary_table("Green-Rice verify", rows))
        fails = [r for r in rows if r[1].startswith("FAIL")]
        if fails:
            warn(
                f"{len(fails)} check(s) failed — see above. Configs are still in place."
            )
        else:
            ok("All checks passed — log out/in (or reboot) to apply Hyprland + GTK.")
    console.print()
    section("Done")
    info("Install state saved at ~/.local/state/green-rice/state.json")
    info("Backups kept at ~/.local/state/green-rice/backups/")
    info("Re-run anytime — already-done steps are skipped (idempotent).")
    info("Rollback:  green-rice-install --rollback")
    console.print()


def run_rollback(args) -> int:
    backup = BackupManager()
    if args.list_backups:
        backs = backup.list_backups()
        if not backs:
            info("no backups found")
            return 0
        console.print("Available backups (newest first):")
        for b in backs:
            console.print(f"  • {b.name}")
        return 0
    target = args.rollback or "latest"
    if target == "latest":
        backs = backup.list_backups()
        if not backs:
            err("no backups to roll back to")
            return 1
        archive = backs[0]
    else:
        archive = backup.backups_dir / target
        if not archive.exists():
            # try matching by prefix
            matches = [b for b in backup.list_backups() if target in b.name]
            archive = matches[0] if matches else None
        if not archive or not archive.exists():
            err(f"backup not found: {target}")
            return 1
    if not confirm(f"Restore {archive.name} over your current configs?", default=False):
        warn("rollback cancelled")
        return 1
    if backup.restore(archive):
        ok("rollback complete — log out/in to restore previous desktop")
        return 0
    return 1


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.state:
        state = InstallState()
        rows = state.summary()
        if not rows:
            info("nothing installed yet (fresh state)")
        else:
            from .ui import summary_table

            console.print(summary_table("Install state", rows))
        return 0

    backup = BackupManager()
    if args.list_backups:
        return run_rollback(args)

    if args.rollback is not None:
        return run_rollback(args)

    sys_info = detect()
    pm = PackageManager(sys_info.distro_id, sys_info.sudo_passwordless)
    state = InstallState()
    ctx = InstallContext(sys_info, pm, state, backup, dry=args.dry_run)

    if args.yes:
        # non-interactive: select all (minus skipped)
        selected = list(DEFAULT_SELECTED)
        if args.skip_packages:
            selected.remove("packages")
        if args.skip_fonts:
            selected.remove("fonts")
        ctx.selected = set(selected)
        # run directly without TUI menu
        section("Non-interactive install")
        console.print(f"components: {', '.join(sorted(ctx.selected))}")
        from .ui import progress_bar

        progress = progress_bar()
        with progress:
            for idx, key in enumerate(ctx.selected, 1):
                progress.add_task(f"[{idx}/{len(ctx.selected)}] {key}", total=1)
                step = STEP_REGISTRY[key]
                try:
                    success, message = step(ctx)
                except Exception as exc:
                    success, message = False, str(exc)
                ok(f"{key}: {message}") if success else err(f"{key}: {message}")
        return 0

    run_interactive(ctx, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
