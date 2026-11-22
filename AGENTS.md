# Green-Rice — AGENTS.md

This file tells coding agents (Claude Code, Codex, etc.) how to work with this repo.

## Repo purpose

Green-Rice is a Hyprland "Miasma" rice (dotfiles) + an **ultra-smart TUI installer** written in Python + Rich. Goal: install, verify, and roll back the desktop — better than OMARCHY 4.5's installer.

## Key directories

```
palette/colors.conf   single source of truth (hex palette)
templates/            per-app {{token}} templates
build.sh              renders templates -> dist/
install.sh            links/copies dist/ into ~/.config
installer/            TUI installer package (Python + Rich)
  __main__.py         entry point (python3 -m installer.__main__)
  green-rice-install  executable bash shim
  cli.py              argparse flags
  ui.py               Rich TUI: banner, swatches, prompts, progress
  detector.py         system detection (distro/WM/pkg-mgr/fonts)
  backup.py           timestamped tar.zst backups + restore
  packages.py         pacman/apt/dnf/brew + AUR abstraction
  state.py            idempotency state file
  steps.py            install steps (packages→fonts→dotfiles→apps→verify)
  verify.py           post-install per-check pass/fail
wallpapers/           Miasma wallpaper set
scripts/              power/bg/audio menus, smart-kill, sync-hypr-lua
assets/               Repo screenshots (hero-banner, tui-preview, desktop-preview)
docs/                 INSTALL.md
```

## Installer entry points

- `./installer/green-rice-install` (interactive TUI)
- `./installer/green-rice-install --dry-run` (preview, no changes)
- `./installer/green-rice-install -y` (non-interactive full install)
- `./installer/green-rice-install --rollback` (restore latest backup)
- `python3 -m installer.__main__` (same as the shim, from repo root)

## Component sets (installer)

packages fonts dotfiles hypr-lua firefox obsidian vscode vencord steam wallpapers scripts verify

## Conventions

- Palette lives ONLY in `palette/colors.conf`; templates use `{{key}}` / `{{dec:key}}`.
- `dist/` is generated — git-ignored, never edit directly.
- The installer is idempotent: re-running skips steps marked done in `~/.local/state/green-rice/state.json`.
- Backups: `~/.local/state/green-rice/backups/` (timestamped tar.zst).
- All installer output must go through `installer/ui.py` (Rich console with Miasma theme) — no bare `print()`.

## Testing

- `python3 -m py_compile installer/*.py` — syntax check
- `./installer/green-rice-install --help` — CLI check
- `./installer/green-rice-install --state` — state check
- Full install needs a TTY (interactive prompts) — use `--dry-run -y` to smoke-test without changes.

## When changing the rice

1. Edit `palette/colors.conf` and/or `templates/*`
2. `./build.sh all` then `./install.sh link`
3. Commit templates + palette, NOT `dist/`
