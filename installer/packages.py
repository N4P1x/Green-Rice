"""Package installation with distro-aware package-manager abstraction.

Best-effort: never aborts the install. On Arch uses pacman (+yay/paru AUR),
else prints a friendly "install these yourself" list.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from typing import Iterable

from rich.console import Console

from .ui import err, info, ok, warn

console = Console()


@dataclass
class PkgSet:
    name: str
    pkgs: list[str]
    aur: bool = False  # needs an AUR helper (yay/paru)


# Core Green-Rice package sets (Arch names). Users on other distros get the list.
ARCH_PACKAGES = [
    PkgSet(
        "wm",
        ["hyprland", "uwsm", "hyprlang2lua", "hyprpaper", "hyprlock", "hypridle"],
        aur=True,
    ),
    PkgSet(
        "terminal",
        ["kitty", "alacritty"],
    ),
    PkgSet("bar", ["waybar", "wofi", "mako"]),
    PkgSet(
        "system",
        [
            "polkit-kde-agent",
            "dolphin",
            "firefox",
            "obsidian",
            "code",
            "btop",
            "nvpy",
            "grim",
            "slurp",
            "wl-clipboard",
            "brightnessctl",
            "playerctl",
            "libnotify",
            "networkmanager",
            "xdg-desktop-portal-hyprland",
            "pipewire",
            "pipewire-pulse",
            "wireplumber",
        ],
    ),
    PkgSet(
        "fonts",
        [
            "noto-fonts",
            "noto-fonts-emoji",
            "ttf-jetbrains-mono-nerd",
        ],
    ),
]


def _has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _run(cmd: list[str], dry: bool = False) -> tuple[bool, str]:
    if dry:
        return True, "[dry] " + " ".join(cmd)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return proc.returncode == 0, proc.stderr.strip() or proc.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "command timed out"
    except FileNotFoundError:
        return False, "command not found"
    except Exception as exc:
        return False, str(exc)


class PackageManager:
    """Abstraction over pacman/apt/dnf/brew."""

    def __init__(self, distro_id: str, sudo_nopw: bool):
        self.distro_id = distro_id
        self.sudo_nopw = sudo_nopw
        self.mgr = self._pick()

    def _pick(self) -> str:
        if _has("pacman"):
            return "pacman"
        if _has("apt"):
            return "apt"
        if _has("dnf"):
            return "dnf"
        if _has("brew"):
            return "brew"
        return "none"

    def aur_helper(self) -> str | None:
        for h in ("yay", "paru"):
            if _has(h):
                return h
        return None

    def update(self, dry: bool = False) -> bool:
        if self.mgr == "pacman" and self.sudo_nopw:
            ok_run, _ = _run(["sudo", "pacman", "-Sy", "--needed", "--noconfirm"], dry)
            return ok_run
        return True

    def install(self, pkgs: Iterable[str], dry: bool = False) -> tuple[bool, str]:
        pkgs = list(pkgs)
        if not pkgs:
            return True, "nothing to install"
        if self.mgr == "pacman":
            cmd = ["sudo", "pacman", "-S", "--needed", "--noconfirm", *pkgs]
            if not self.sudo_nopw:
                return False, "no passwordless sudo — install manually"
        elif self.mgr == "apt":
            cmd = ["sudo", "apt-get", "install", "-y", *pkgs]
        elif self.mgr == "dnf":
            cmd = ["sudo", "dnf", "install", "-y", *pkgs]
        elif self.mgr == "brew":
            cmd = ["brew", "install", *pkgs]
        else:
            return False, f"no package manager ({self.mgr})"
        ok_run, out = _run(cmd, dry)
        return ok_run, out

    def install_aur(self, pkgs: Iterable[str], dry: bool = False) -> tuple[bool, str]:
        pkgs = list(pkgs)
        if not pkgs:
            return True, "nothing to install"
        helper = self.aur_helper()
        if not helper:
            return False, "no AUR helper (yay/paru) found"
        cmd = [helper, "-S", "--needed", "--noconfirm", *pkgs]
        return _run(cmd, dry)

    def missing(self, pkgs: Iterable[str]) -> list[str]:
        """Return pkgs that aren't installed (pacman -Q check)."""
        if self.mgr != "pacman":
            return list(pkgs)  # can't easily check elsewhere; assume missing
        out = subprocess.run(["pacman", "-Q"], capture_output=True, text=True).stdout
        installed = {line.split()[0] for line in out.splitlines()}
        return [p for p in pkgs if p not in installed]
