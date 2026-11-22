"""Green-Rice — proper full-screen TUI installer built with Textual.

A real terminal UI (not stdout printing) with:
  * full-screen layout: header + sidebar + main + footer
  * keyboard-navigable component selection (checkboxes)
  * live Miasma palette preview with color swatches
  * system detection panel
  * install / dry-run / verify / rollback actions
  * live log output
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widgets import (
    Checkbox,
    Footer,
    Header,
    Label,
    Static,
    Button,
    DataTable,
)

from .backup import BackupManager
from .detector import detect, render_info
from .packages import PackageManager
from .state import InstallState
from .steps import COMPONENT_SETS, STEP_REGISTRY, InstallContext
from .ui import miasma_theme

DEFAULT_SELECTED: list[str] = list(COMPONENT_SETS)

REPO = Path(__file__).resolve().parent.parent
HOME = Path.home()
CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config"))


# ---------------------------------------------------------------------------
# Widgets
# ---------------------------------------------------------------------------


class PaletteSwatch(Static):
    """A single color swatch with its hex value."""

    def __init__(self, role: str, hexv: str):
        super().__init__()
        self.role = role
        self.hexv = hexv

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static("████", classes=f"swatch-{self.hexv}")
            yield Label(f"{self.role}", classes="swatch-role")
            yield Label(f"#{self.hexv}", classes="swatch-hex")


class PalettePanel(Static):
    """Live Miasma palette preview."""

    def compose(self) -> ComposeResult:
        yield Label("Miasma Palette", classes="panel-title")
        palette = [
            ("bg", "222222"),
            ("bg_panel", "1c1c1c"),
            ("accent", "78824b"),
            ("fg", "c2c2b0"),
            ("fg_bright", "d7c483"),
            ("highlight", "e4c47a"),
        ]
        for role, hexv in palette:
            yield PaletteSwatch(role, hexv)


class SystemPanel(Static):
    """System detection display."""

    def compose(self) -> ComposeResult:
        yield Label("System Detected", classes="panel-title")
        yield Static("", id="system-info", classes="system-info")


class ComponentList(VerticalScroll):
    """Sidebar list of installable components with checkboxes."""

    def __init__(self, selected: set[str]):
        super().__init__()
        self.selected = selected

    def compose(self) -> ComposeResult:
        yield Label("Components", classes="panel-title")
        for key in COMPONENT_SETS:
            checked = key in self.selected
            yield Checkbox(key.replace("-", " ").title(), value=checked, id=f"cb-{key}")


class LogPanel(VerticalScroll):
    """Live install log output."""

    def __init__(self):
        super().__init__()
        self._lines: list[str] = []

    def log(self, msg: str, style: str = "default") -> None:
        self._lines.append(f"[{style}]{msg}[/{style}]")
        if len(self._lines) > 200:
            self._lines = self._lines[-200:]
        self.update("\n".join(self._lines))
        self.scroll_end()

    def clear(self) -> None:
        self._lines = []
        self.update("")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------


class GreenRiceInstaller(App):
    """Full-screen TUI installer for Green-Rice."""

    CSS = """
    Screen {
        layout: vertical;
        background: #101010;
        color: #c2c2b0;
    }

    #header {
        dock: top;
        height: 8;
        background: #1c1c1c;
        border: solid #78824b;
        padding: 1 2;
    }

    #banner-title {
        text-style: bold;
        color: #c2c2b0;
        text-align: left;
    }

    #banner-sub {
        color: #78824b;
        text-align: left;
    }

    #main {
        layout: horizontal;
        height: 1fr;
    }

    #sidebar {
        width: 30;
        background: #1a1a16;
        border: solid #33332e;
        padding: 1;
    }

    #main-panel {
        width: 1fr;
        background: #101010;
        padding: 1;
    }

    #footer-bar {
        dock: bottom;
        height: 4;
        background: #1c1c1c;
        border: solid #78824b;
        padding: 1 2;
    }

    .panel-title {
        text-style: bold;
        color: #e4c47a;
        margin-bottom: 1;
    }

    .system-info {
        color: #8a8a7e;
        text-style: monospace;
        margin-bottom: 1;
    }

    .swatch-role {
        color: #c2c2b0;
        width: 16;
    }

    .swatch-hex {
        color: #d7c483;
        text-style: monospace;
    }

    Button {
        margin: 0 1;
    }

    #log {
        height: 1fr;
        border: solid #33332e;
        background: #0a0a08;
        padding: 1;
        overflow-y: scroll;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("i", "install", "Install", show=True),
        Binding("d", "dry_run", "Dry Run", show=True),
        Binding("v", "verify", "Verify", show=True),
        Binding("r", "rollback", "Rollback", show=True),
        Binding("up", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("space", "toggle", "Toggle", show=False),
        Binding("enter", "confirm", "Confirm", show=False),
    ]

    selected: reactive[set[str]] = reactive(set(DEFAULT_SELECTED))
    dry_run: reactive[bool] = reactive(False)

    def __init__(self):
        super().__init__()
        self.sys_info = detect()
        self.pm = PackageManager(
            self.sys_info.distro_id, self.sys_info.sudo_passwordless
        )
        self.state = InstallState()
        self.backup = BackupManager()
        self.log_panel: LogPanel | None = None

    # ------------------------------------------------------------------
    # Compose
    # ------------------------------------------------------------------
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Container(id="header"):
            yield Static("GREEN-RICE", id="banner-title", classes="banner-title")
            yield Static(
                "Miasma Hyprland Rice  ·  Ultra-Smart TUI Installer  ·  Better than OMARCHY 4.5",
                id="banner-sub",
                classes="banner-sub",
            )

        with Container(id="main"):
            with Vertical(id="sidebar"):
                yield ComponentList(self.selected)
            with VerticalScroll(id="main-panel"):
                yield SystemPanel()
                yield PalettePanel()
                yield Label("Actions", classes="panel-title")
                with Horizontal():
                    yield Button("Install", id="btn-install", variant="success")
                    yield Button("Dry Run", id="btn-dry", variant="warning")
                    yield Button("Verify", id="btn-verify", variant="default")
                    yield Button("Rollback", id="btn-rollback", variant="error")
                yield Label("Install Log", classes="panel-title")
                yield LogPanel(id="log")

        yield Footer()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def on_mount(self) -> None:
        self.log_panel = self.query_one("#log", LogPanel)
        sys_panel = self.query_one(SystemPanel)
        info_text = render_info(self.sys_info)
        sys_panel.query_one("#system-info", Static).update(info_text)
        self.log("System detected — ready to install.")
        self.log(f"Distro: {self.sys_info.distro_name} ({self.sys_info.distro_id})")
        self.log(f"WM: {self.sys_info.wm} | Pkg: {self.sys_info.package_manager}")
        self.log(f"Selected: {', '.join(sorted(self.selected)) or 'none'}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def log(self, msg: str, style: str = "default") -> None:
        if self.log_panel:
            self.log_panel.log(msg, style)

    def get_selected_keys(self) -> list[str]:
        """Read checkbox states from the sidebar."""
        keys: list[str] = []
        for key in COMPONENT_SETS:
            cb = self.query_one(f"#cb-{key}", Checkbox)
            if cb.value:
                keys.append(key)
        return keys

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_install(self) -> None:
        self.run_install(dry=False)

    def action_dry_run(self) -> None:
        self.run_install(dry=True)

    def action_verify(self) -> None:
        self.log("Running verification…", "warn")
        asyncio.create_task(self._run_verify())

    def action_rollback(self) -> None:
        self.log("Rollback: restoring latest backup…", "warn")
        backs = self.backup.list_backups()
        if not backs:
            self.log("No backups found.", "err")
            return
        self.backup.restore(backs[0])
        self.log("Rollback complete — log out/in to restore desktop.", "ok")

    def action_cursor_up(self) -> None:
        self.focus_previous()

    def action_cursor_down(self) -> None:
        self.focus_next()

    def action_toggle(self) -> None:
        focused = self.focused
        if isinstance(focused, Checkbox):
            focused.toggle()

    def action_confirm(self) -> None:
        pass

    async def _run_verify(self) -> None:
        from .verify import check_command, check_file

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
        ]
        rows = [(label, result) for label, (_, result) in checks]
        fails = [r for r in rows if r[1].startswith("FAIL")]
        for label, result in rows:
            style = (
                "ok"
                if result.startswith("ok")
                else ("warn" if result.startswith("skip") else "err")
            )
            self.log(f"{label}: {result}", style)
        if fails:
            self.log(f"{len(fails)} check(s) failed.", "err")
        else:
            self.log("All checks passed.", "ok")

    # ------------------------------------------------------------------
    # Install
    # ------------------------------------------------------------------
    def run_install(self, dry: bool) -> None:
        self.dry_run = dry
        selected = self.get_selected_keys()
        self.selected = set(selected)
        self.log(f"{'DRY RUN ' if dry else ''}Install starting…", "warn")
        self.log(f"Components: {', '.join(selected) or 'none'}")
        asyncio.create_task(self._install_async(selected, dry))

    async def _install_async(self, selected: list[str], dry: bool) -> None:
        ctx = InstallContext(
            self.sys_info, self.pm, self.state, self.backup, dry=dry, selected=selected
        )

        # Pre-install backup
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
        if pre_targets and not dry:
            self.backup.snapshot("pre-install", pre_targets)
            self.log("Smart backup created.", "ok")

        # Run steps
        total = len(selected)
        for idx, key in enumerate(selected, 1):
            self.log(f"[{idx}/{total}] {key}…", "warn")
            step = STEP_REGISTRY[key]
            try:
                success, message = step(ctx)
            except Exception as exc:
                success, message = False, f"step raised: {exc}"
            if success:
                self.log(f"  ✓ {key}: {message}", "ok")
            else:
                self.log(f"  ✗ {key}: {message}", "err")

        # Verify
        if "verify" in selected:
            self.log("Running verification…", "warn")
            from .verify import check_command, check_file

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
            rows = [(label, result) for label, (_, result) in checks]
            for label, result in rows:
                style = (
                    "ok"
                    if result.startswith("ok")
                    else ("warn" if result.startswith("skip") else "err")
                )
                self.log(f"  {label}: {result}", style)

        self.log("Install complete.", "ok")
        self.log("Log out/in (or reboot) to apply Hyprland + GTK.", "warn")

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------
    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "btn-install":
            self.action_install()
        elif btn_id == "btn-dry":
            self.action_dry_run()
        elif btn_id == "btn-verify":
            self.action_verify()
        elif btn_id == "btn-rollback":
            self.action_rollback()
