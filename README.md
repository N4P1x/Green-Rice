# Green-Rice

<p align="center">
  <img src="assets/desktop-real.png" width="100%" alt="Green-Rice desktop" />
</p>

Miasma Hyprland rice with a TUI installer.

- `palette/colors.conf` — single source of truth (hex palette, no `#`)
- `templates/` — per-app configs with `{{token}}` placeholders
- `build.sh` — renders `templates/` → `dist/`
- `install.sh` — links/copies `dist/` into `~/.config`
- `installer/` — TUI installer (Python + Textual)
- `scripts/` — power-menu, bg-menu, audio-menu, smart-kill, sync-hypr-lua
- `wallpapers/` — Miasma wallpaper set

---

## Install

```sh
git clone https://github.com/N4P1x/Green-Rice.git
cd Green-Rice
./installer/green-rice-install
```

Flags:

| Flag                  | What it does                  |
| --------------------- | ----------------------------- |
| `--dry-run`           | Preview without changes       |
| `-y` / `--yes`        | Non-interactive install       |
| `--select A B C`      | Install only these components |
| `--skip-packages`     | Skip package installation     |
| `--skip-fonts`        | Skip font installation        |
| `--rollback [BACKUP]` | Restore configs from a backup |
| `--list-backups`      | List available backups        |
| `--state`             | Show install-state log        |

Components: packages, fonts, dotfiles, hypr-lua, firefox, obsidian, vscode, vencord, steam, wallpapers, scripts, verify.

---

## Manual (without TUI)

```sh
./build.sh          # render templates → dist/
./install.sh dry    # preview symlinks
./install.sh link   # symlink dist/ into ~/.config
# then reload Hyprland, restart waybar + mako
```

Re-colour: edit `palette/colors.conf`, then `./build.sh all && ./install.sh link`.

---

## Rollback

Backups live in `~/.local/state/green-rice/backups/`.

```sh
./installer/green-rice-install --rollback
```

---

## Requirements

- Arch Linux — `pacman`, optional `yay`/`paru` for AUR
- Hyprland ≥ 0.56
- `python3` + `textual` (TUI installer)
- `git`, `curl`, `unzip`, `zstd`, `fc-cache`

---

## License

MIT — see [LICENSE](LICENSE).
