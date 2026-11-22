"""Theme helpers for the Green-Rice installer.

Miasma palette colors and ok/warn/err/info styling helpers.
"""

from __future__ import annotations

from typing import Iterable, Sequence

from rich.align import Align
from rich.box import ROUNDED
from rich.color import Color
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

# --- Miasma palette (single source of truth, mirrored from palette/colors.conf) ---
MIASMA = {
    # surfaces
    "bg": "222222",
    "bg_darker": "101010",
    "bg_dark": "151515",
    "bg_lighter": "242d1d",
    "bg_panel": "1c1c1c",
    # text
    "fg": "c2c2b0",
    "fg_muted": "8a8a7e",
    "fg_dim": "666666",
    "fg_bright": "d7c483",
    # accent
    "accent": "78824b",
    "accent_dark": "3c4125",
    "accent_mid": "43492a",
    # selection / highlight
    "selection": "383838",
    "selection_fg": "c2c2b0",
    "highlight": "e4c47a",
    "highlight_fg": "000000",
}


def miasma_theme() -> Theme:
    """A Rich Theme whose styles are named after Miasma palette keys."""
    return Theme(
        {
            "miasma.bg": f"#{MIASMA['bg']}",
            "miasma.fg": f"#{MIASMA['fg']}",
            "miasma.fg_muted": f"#{MIASMA['fg_muted']}",
            "miasma.fg_bright": f"#{MIASMA['fg_bright']}",
            "miasma.accent": f"#{MIASMA['accent']}",
            "miasma.highlight": f"#{MIASMA['highlight']}",
            "miasma.bg_panel": f"#{MIASMA['bg_panel']}",
            "ok": f"#{MIASMA['accent']}",
            "warn": f"#{MIASMA['fg_bright']}",
            "err": "#bb7744",
            "muted": f"#{MIASMA['fg_muted']}",
        }
    )


# A single shared console so every panel/spinner uses the same theme.
console = Console(theme=miasma_theme(), force_terminal=True)


def banner() -> None:
    """Print the welcome banner."""
    title = Text.assemble(
        ("  GREEN-RICE  ", "bold miasma.fg on miasma.bg_panel"),
        ("   TUI installer   ", "miasma.accent"),
    )
    subtitle = Text(
        "Miasma Hyprland rice  •  installs, verifies, rolls back",
        style="miasma.fg_muted",
    )
    panel = Panel(
        Align.center(Group(title, Text("", style=""), subtitle), vertical="middle"),
        box=ROUNDED,
        border_style="miasma.accent",
        padding=(1, 4),
    )
    console.print()
    console.print(panel)
    console.print()


def section(title: str) -> None:
    """Print a section header."""
    console.print()
    console.print(Text.assemble("▸ ", "bold miasma.accent", (title, "bold miasma.fg")))
    console.print(Text("─" * min(len(title) + 2, 60), style="miasma.fg_dim"))


def info(msg: str) -> None:
    console.print(f"  [miasma.fg_mixed]→[/]  {msg}")


def ok(msg: str) -> None:
    console.print(f"  [ok]✓[/]  {msg}")


def warn(msg: str) -> None:
    console.print(f"  [warn]⚠[/]  {msg}")


def err(msg: str) -> None:
    console.print(f"  [err]✗[/]  {msg}")


def color_swatches() -> Table:
    """A table of Miasma color swatches so the user previews the theme."""
    table = Table(
        title="Miasma palette preview", box=ROUNDED, border_style="miasma.accent"
    )
    table.add_column("Role", style="miasma.fg_muted", width=16)
    table.add_column("Swatch", width=10)
    table.add_column("Hex", style="miasma.fg_bright")

    rows = [
        ("bg (surface)", "bg"),
        ("accent (olive)", "accent"),
        ("fg (text)", "fg"),
        ("fg_bright", "fg_bright"),
        ("highlight", "highlight"),
        ("bg_panel", "bg_panel"),
    ]
    for role, key in rows:
        hexv = MIASMA[key]
        swatch = Text("█" * 8, style=f"#{hexv} on #{hexv}")
        table.add_row(role, swatch, f"#{hexv}")
    return table


def confirm(prompt: str, default: bool = False) -> bool:
    return Confirm.ask(prompt, default=default, console=console)


def prompt(prompt: str, default: str | None = None) -> str:
    return Prompt.ask(prompt, default=default, console=console)


def int_prompt(prompt: str, default: int | None = None) -> int:
    return IntPrompt.ask(prompt, default=default, console=console)


class ComponentsMenu:
    """Interactive multi-select menu rendered with Rich (works in any terminal)."""

    def __init__(self, items: Sequence[tuple[str, str, bool]]):
        # items: list of (key, label, selected)
        self.items = [[key, label, bool(sel)] for key, label, sel in items]

    def render(self) -> Table:
        table = Table(
            box=ROUNDED,
            border_style="miasma.accent",
            header_style="bold",
        )
        table.add_column("#", width=4, style="miasma.fg_muted")
        table.add_column("Pick", width=6, style="miasma.accent")
        table.add_column("Component", style="miasma.fg")
        table.add_column("What it does", style="miasma.fg_muted")
        for i, (key, label, sel) in enumerate(self.items, 1):
            pick = "[x]" if sel else "[ ]"
            pick_style = "ok" if sel else "muted"
            table.add_row(str(i), Text(pick, style=pick_style), label, self._desc(key))
        return table

    @staticmethod
    def _desc(key: str) -> str:
        descs = {
            "packages": "System packages (hyprland, kitty, waybar, wofi, fonts, …)",
            "fonts": "JetBrainsMono Nerd Font + Noto Color Emoji (user-local, no sudo)",
            "dotfiles": "Build + link all Miasma configs into ~/.config",
            "hypr-lua": "Hyprland Lua theme + live keybinding sync",
            "firefox": "Firefox userChrome.css + dark-theme prefs",
            "obsidian": "Obsidian miasma.css snippet for your vault",
            "vscode": "VS Code Miasma colour theme",
            "vencord": "Vencord Discord theme",
            "steam": "Steam Adwaita skin CSS",
            "wallpapers": "Miasma wallpaper set + hyprpaper config",
            "scripts": "power/bg/audio menus + smart-kill to ~/.local/bin",
            "verify": "Run post-install verification checks",
        }
        return descs.get(key, "")

    def run(self) -> list[str]:
        """Loop until the user is done. Returns the list of selected keys."""
        while True:
            console.clear()
            banner()
            section("Choose what to install")
            console.print(self.render())
            console.print()
            console.print(
                "  [miasma.fg_muted]Tip:[/] type a number to toggle, "
                "[miasma.accent]a[/] = all, [miasma.accent]n[/] = none, "
                "[miasma.accent]d[/] = done[/]"
            )
            choice = prompt("Selection", default="d").strip().lower()
            if choice == "d":
                break
            if choice == "a":
                for item in self.items:
                    item[2] = True
                continue
            if choice == "n":
                for item in self.items:
                    item[2] = False
                continue
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.items):
                    self.items[idx][2] = not self.items[idx][2]
            except ValueError:
                warn("Enter a number, 'a', 'n', or 'd'.")
        return [key for key, _, sel in self.items if sel]


def progress_bar() -> Progress:
    """A styled Progress instance for install steps."""
    return Progress(
        SpinnerColumn(spinner_name="dots", style="miasma.accent"),
        TextColumn("{task.description}", style="miasma.fg"),
        BarColumn(
            bar_width=40, style="miasma.bg_panel", complete_style="miasma.accent"
        ),
        TaskProgressColumn(style="miasma.fg_bright"),
        TimeRemainingColumn(style="miasma.fg_muted"),
        console=console,
        transient=False,
    )


def summary_table(title: str, rows: Iterable[tuple[str, str]]) -> Table:
    table = Table(title=title, box=ROUNDED, border_style="miasma.accent")
    table.add_column("Check", style="miasma.fg")
    table.add_column("Result", style="miasma.fg_muted")
    for check, result in rows:
        style = (
            "ok"
            if result.startswith("ok")
            else ("warn" if result.startswith("skip") else "err")
        )
        icon = (
            "✓"
            if result.startswith("ok")
            else ("○" if result.startswith("skip") else "✗")
        )
        table.add_row(check, Text.assemble((icon + "  ", style), (result, style)))
    return table


def ask_rollback(backup_dir: str) -> bool:
    return Confirm.ask(
        f"[warn]Roll back[/] to the backup at {backup_dir} and restore your previous configs?",
        default=False,
        console=console,
    )
