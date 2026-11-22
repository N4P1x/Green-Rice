"""Command-line interface for the Green-Rice installer."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from . import __prog__, __version__


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog=__prog__,
        description="Green-Rice — ultra smart TUI installer for the Miasma Hyprland rice.",
    )
    p.add_argument("--version", action="version", version=f"{__prog__} {__version__}")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="preview everything without making changes",
    )
    p.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="non-interactive: accept defaults and run the full install",
    )
    p.add_argument(
        "--select",
        nargs="*",
        help="component sets to install (space-separated). Default: all. "
        f"Choices: packages fonts dotfiles hypr-lua firefox obsidian vscode vencord steam wallpapers scripts verify",
    )
    p.add_argument(
        "--skip-packages",
        action="store_true",
        help="skip system package installation",
    )
    p.add_argument(
        "--skip-fonts",
        action="store_true",
        help="skip font installation",
    )
    p.add_argument(
        "--vault",
        metavar="PATH",
        help="Obsidian vault path (default: auto-detect ~/Mind/MIND)",
    )
    p.add_argument(
        "--rollback",
        metavar="BACKUP",
        nargs="?",
        const="latest",
        help="restore configs from a backup (default: latest)",
    )
    p.add_argument(
        "--list-backups",
        action="store_true",
        help="list available backups and exit",
    )
    p.add_argument(
        "--state",
        action="store_true",
        help="show install state (idempotency log) and exit",
    )
    return p


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)
