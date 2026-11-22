"""Install-state tracking for idempotency and rollback.

A small JSON state file records which component sets were installed and when,
so re-running is safe (skips already-done work) and rollback knows what to undo.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .ui import info, ok, warn

STATE_FILENAME = "state.json"


class InstallState:
    def __init__(self, base: Path | None = None):
        self.base = base or Path.home() / ".local" / "state" / "green-rice"
        self.base.mkdir(parents=True, exist_ok=True)
        self.path = self.base / STATE_FILENAME
        self.data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                warn("state file corrupt — starting fresh")
        return {"version": 1, "installed": {}, "created": datetime.now().isoformat()}

    def save(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def is_done(self, key: str) -> bool:
        return bool(self.data.get("installed", {}).get(key, {}).get("done"))

    def mark(self, key: str, detail: str = "") -> None:
        self.data.setdefault("installed", {})[key] = {
            "done": True,
            "at": datetime.now().isoformat(),
            "detail": detail,
        }
        self.save()
        ok(f"state: {key} marked done")

    def summary(self) -> list[tuple[str, str]]:
        rows = []
        for key, val in self.data.get("installed", {}).items():
            rows.append((key, "done" if val.get("done") else "pending"))
        return rows
