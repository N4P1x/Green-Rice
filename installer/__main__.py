"""Green-Rice installer entry point.

Run:  python3 -m installer.__main__          # full-screen Textual TUI
      ./installer/green-rice-install          # same (bash shim)
      ./installer/green-rice-install --dry-run -y   # non-interactive
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import __prog__, __version__
from .app import GreenRiceInstaller
from .backup import BackupManager
from .cli import parse_args
from .detector import detect
from .packages import PackageManager
from .state import InstallState
from .steps import COMPONENT_SETS, STEP_REGISTRY, InstallContext
from .ui import err, info, ok, summary_table, warn
import os


def run_non_interactive(args) -> int:
    """Run install without TUI (for -y / --select)."""
    sys_info = detect()
    pm = PackageManager(sys_info.distro_id, sys_info.sudo_passwordless)
    state = InstallState()
    backup = BackupManager()

    selected = list(COMPONENT_SETS)
    if args.select:
        selected = args.select
    if args.skip_packages:
        selected = [s for s in selected if s != "packages"]
    if args.skip_fonts:
        selected = [s for s in selected if s != "fonts"]

    ctx = InstallContext(
        sys_info, pm, state, backup, dry=args.dry_run, selected=selected
    )

    info(f"Non-interactive install: {', '.join(selected)}")

    # Pre-install backup
    HOME = Path.home()
    CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))
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
        backup.snapshot("pre-install", pre_targets)
        ok("Smart backup created.")

    for key in selected:
        step = STEP_REGISTRY[key]
        try:
            success, message = step(ctx)
        except Exception as exc:
            success, message = False, str(exc)
        ok(f"{key}: {message}") if success else err(f"{key}: {message}")

    return 0


import os  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.state:
        state = InstallState()
        rows = state.summary()
        if not rows:
            info("nothing installed yet (fresh state)")
        else:
            console = __import__("rich.console", fromlist=["Console"]).Console()
            from .ui import summary_table

            console.print(summary_table("Install state", rows))
        return 0

    backup = BackupManager()
    if args.list_backups:
        backs = backup.list_backups()
        if not backs:
            info("no backups found")
            return 0
        console = __import__("rich.console", fromlist=["Console"]).Console()
        console.print("Available backups (newest first):")
        for b in backs:
            console.print(f"  • {b.name}")
        return 0

    if args.rollback is not None:
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
                matches = [b for b in backup.list_backups() if target in b.name]
                archive = matches[0] if matches else None
            if not archive or not archive.exists():
                err(f"backup not found: {target}")
                return 1
        if not confirm_rollback(f"Restore {archive.name}?"):
            warn("rollback cancelled")
            return 1
        if backup.restore(archive):
            ok("rollback complete — log out/in to restore previous desktop")
            return 0
        return 1

    if args.yes:
        return run_non_interactive(args)

    # Full-screen Textual TUI
    app = GreenRiceInstaller()
    return app.run()


def confirm_rollback(prompt: str) -> bool:
    try:
        ans = input(f"{prompt} [y/N] ").strip().lower()
        return ans == "y" or ans == "yes"
    except (EOFError, KeyboardInterrupt):
        return False


if __name__ == "__main__":
    sys.exit(main())
