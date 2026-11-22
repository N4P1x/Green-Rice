"""Post-install verification: per-check pass/fail against the live system."""

from __future__ import annotations

import shutil
import subprocess
from typing import Iterable

from .ui import err, ok, warn

FONTS = ["JetBrainsMono Nerd Font Mono", "Noto Color Emoji"]


def _run(cmd: list[str]) -> tuple[bool, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
        return proc.returncode == 0, (proc.stdout + proc.stderr).strip()
    except FileNotFoundError:
        return False, "command not found"
    except subprocess.TimeoutExpired:
        return False, "timed out"
    except Exception as exc:
        return False, str(exc)


def check_command(name: str, cmd: str) -> tuple[str, str]:
    ok_run, _ = _run(["sh", "-c", f"command -v {cmd} >/dev/null"])
    return (name, "ok: installed") if ok_run else (name, "FAIL: not installed")


def check_file(path: str) -> tuple[str, str]:
    import os

    return (path, "ok: present") if os.path.exists(path) else (path, "FAIL: missing")


def check_symlink(path: str, target: str | None = None) -> tuple[str, str]:
    import os

    if not os.path.islink(path):
        return (path, "FAIL: not a symlink")
    if target is None:
        return (path, "ok: symlink")
    try:
        real = os.readlink(path)
        if target in real:
            return (path, "ok: symlink")
        return (path, f"FAIL: points to {real}")
    except OSError:
        return (path, "FAIL: unreadable")


def check_font(font: str) -> tuple[str, str]:
    ok_run, out = _run(["fc-match", font])
    if ok_run and font.lower() in out.lower():
        return (font, "ok: installed")
    return (font, "FAIL: not found")


def check_hypr_config() -> tuple[str, str]:
    import os

    p = os.path.expanduser("~/.config/hypr/hyprland.conf")
    if os.path.islink(p) or os.path.exists(p):
        return ("hyprland.conf", "ok: linked")
    return ("hyprland.conf", "FAIL: missing")


def run_checks(checks: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    """Run a list of (label, result) pairs — used by the verify step."""
    return list(checks)
