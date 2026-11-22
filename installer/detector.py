"""System detection for the Green-Rice installer.

Detects OS/distro, window manager, shell, package manager, fonts, and
whether the machine is Arch (where package install works best-effort).
Everything is best-effort — missing info never aborts the install.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass, field


def _run(cmd: list[str]) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
        return out.stdout.strip()
    except Exception:
        return ""


def _has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except Exception:
        return ""


@dataclass
class SystemInfo:
    os_name: str = "unknown"
    distro_id: str = "unknown"
    distro_name: str = "unknown"
    arch: str = "unknown"
    kernel: str = "unknown"
    hostname: str = "unknown"
    user: str = "unknown"
    shell: str = "unknown"
    wm: str = "none"
    wm_version: str = "none"
    display_server: str = "unknown"
    package_manager: str = "none"
    aur_helper: str = "none"
    sudo_passwordless: bool = False
    fonts: list[str] = field(default_factory=list)
    hyprland_running: bool = False
    is_arch: bool = False


def detect() -> SystemInfo:
    info = SystemInfo()

    # --- OS / distro ---
    osrel = _read("/etc/os-release")
    for line in osrel.splitlines():
        if line.startswith("ID="):
            info.distro_id = line.split("=", 1)[1].strip('"')
        elif line.startswith("PRETTY_NAME="):
            info.distro_name = line.split("=", 1)[1].strip('"')
        elif line.startswith("NAME=") and not info.distro_name:
            info.distro_name = line.split("=", 1)[1].strip('"')
    info.os_name = info.distro_name or info.distro_id
    info.is_arch = info.distro_id == "arch"

    info.arch = _run(["uname", "-m"]) or "unknown"
    info.kernel = _run(["uname", "-r"]) or "unknown"
    info.hostname = _run(["cat", "/etc/hostname"]) or _run(["hostname"]) or "unknown"
    info.user = os.environ.get("USER") or "unknown"
    info.shell = os.path.basename(os.environ.get("SHELL", "/bin/sh")) or "sh"

    # --- display server / WM ---
    if os.environ.get("WAYLAND_DISPLAY"):
        info.display_server = "Wayland"
    elif os.environ.get("DISPLAY"):
        info.display_server = "X11"
    if _has("hyprctl"):
        info.wm = "Hyprland"
        ver = _run(["hyprctl", "version"])
        if ver:
            info.wm_version = ver.splitlines()[0] if ver.splitlines() else "Hyprland"
        try:
            subprocess.run(
                ["hyprctl", "instances"], capture_output=True, timeout=3, check=True
            )
            info.hyprland_running = True
        except Exception:
            info.hyprland_running = False
    elif _has("swaymsg"):
        info.wm = "Sway"
    elif _has("i3-msg"):
        info.wm = "i3"

    # --- package managers ---
    if _has("pacman"):
        info.package_manager = "pacman"
        if _has("yay"):
            info.aur_helper = "yay"
        elif _has("paru"):
            info.aur_helper = "paru"
    elif _has("apt"):
        info.package_manager = "apt"
    elif _has("dnf"):
        info.package_manager = "dnf"
    elif _has("brew"):
        info.package_manager = "brew"

    info.sudo_passwordless = (
        subprocess.run(
            ["sudo", "-n", "true"], capture_output=True, timeout=3
        ).returncode
        == 0
    )

    # --- fonts ---
    for font in ("JetBrainsMono Nerd Font Mono", "Noto Color Emoji"):
        out = _run(["fc-match", font])
        if out and ("not found" not in out.lower()):
            info.fonts.append(font)

    return info


def render_info(info: SystemInfo) -> str:
    lines = [
        f"  distro    : {info.distro_name} ({info.distro_id})",
        f"  arch      : {info.arch}  kernel {info.kernel}",
        f"  host      : {info.hostname}  user {info.user}",
        f"  shell     : {info.shell}",
        f"  WM        : {info.wm} {info.wm_version}".strip()
        + (f" (running)" if info.hyprland_running else " (not running)"),
        f"  display   : {info.display_server}",
        f"  pkg mgr   : {info.package_manager}"
        + (f" / aur: {info.aur_helper}" if info.aur_helper else ""),
        f"  sudo nopw : {'yes' if info.sudo_passwordless else 'no'}",
        f"  fonts     : {', '.join(info.fonts) if info.fonts else 'none detected'}",
    ]
    return "\n".join(lines)
