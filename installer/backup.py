"""Smart backups: timestamped snapshots of existing configs before any overwrite.

Backups live in ~/.local/state/green-rice/backups/<timestamp>/
A manifest records exactly what was backed up so rollback is exact and safe.
"""

from __future__ import annotations

import shutil
import tarfile
from datetime import datetime
from pathlib import Path
from typing import Iterable

from rich.console import Console

from .ui import err, info, ok, warn

console = Console()


class BackupManager:
    """Manages timestamped backups of files/dirs the installer is about to touch."""

    def __init__(self, base: Path | None = None):
        self.base = base or Path.home() / ".local" / "state" / "green-rice"
        self.backups_dir = self.base / "backups"
        self.state_dir = self.base / "state"
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _stamp(self) -> str:
        return datetime.now().strftime("%Y%m%d-%H%M%S")

    def snapshot(self, label: str, paths: Iterable[Path]) -> Path | None:
        """Back up a list of files/dirs into a dated tar.zst archive.

        Returns the archive path, or None if nothing existed to back up.
        """
        paths = [p for p in paths if p.exists()]
        if not paths:
            return None
        stamp = self._stamp()
        archive = self.backups_dir / f"green-rice-backup-{label}-{stamp}.tar.zst"
        manifest = self.backups_dir / f"green-rice-backup-{label}-{stamp}.manifest"
        backed: list[str] = []
        with tarfile.open(archive, "w:zstd") as tar:
            for p in paths:
                if p.is_dir():
                    for child in p.rglob("*"):
                        try:
                            tar.add(child, arcname=str(child))
                            backed.append(str(child))
                        except Exception:
                            pass
                    tar.add(p, arcname=str(p))
                    backed.append(str(p))
                else:
                    tar.add(p, arcname=str(p))
                    backed.append(str(p))
        manifest.write_text("\n".join(backed) + "\n", encoding="utf-8")
        # latest pointer
        latest = self.backups_dir / f"green-rice-backup-{label}-latest.tar.zst"
        try:
            if latest.exists() or latest.is_symlink():
                latest.unlink()
        except Exception:
            pass
        try:
            latest.symlink_to(archive.name)
        except OSError:
            shutil.copy2(archive, latest)
        info(f"backup: {archive.name} ({len(backed)} entries)")
        return archive

    def list_backups(self) -> list[Path]:
        return sorted(
            self.backups_dir.glob("green-rice-backup-*.tar.zst"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

    def restore(self, archive: Path) -> bool:
        """Extract an archive over the current system (destructive!)."""
        if not archive.exists():
            err(f"backup not found: {archive}")
            return False
        try:
            with tarfile.open(archive, "r:zstd") as tar:
                tar.extractall(path=Path.home(), filter="data")
            ok(f"restored {archive.name} to ~")
            return True
        except Exception as exc:
            err(f"restore failed: {exc}")
            return False

    def record_installed(self, key: str, detail: str = "") -> None:
        """Append to the install-state log for idempotency / rollback reference."""
        log = self.state_dir / "installed.log"
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with log.open("a", encoding="utf-8") as fh:
            fh.write(f"{stamp}  {key}  {detail}\n")

    def installed_log(self) -> str:
        log = self.state_dir / "installed.log"
        return (
            log.read_text(encoding="utf-8")
            if log.exists()
            else "(nothing installed yet)"
        )
