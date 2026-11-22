# Green-Rice

**Green-Rice** is my personal Hyprland rice — the **Miasma** theme — shipped with an **ultra-smart TUI installer** that installs, verifies, and rolls back. Think OMARCHY 4.5's installer, but with a real Rich-powered TUI, interactive component selection, live color swatches, timestamped smart backups, one-command rollback, and idempotent re-runs.

```
cellar-grey #222222 surfaces  ·  pale-linen #c2c2b0 text  ·  moss-olive #78824b accent
soft fogbank animations inside sharp-cornered Hyprland
```

## What's inside

| Part                  | What it is                                                 |
| --------------------- | ---------------------------------------------------------- |
| `palette/colors.conf` | Single source of truth — one hex palette, no `#`           |
| `templates/`          | Per-app configs with `{{token}}` placeholders              |
| `build.sh`            | Renders `templates/` → `dist/`                             |
| `install.sh`          | Links/copies `dist/` into `~/.config`                      |
| `installer/`          | **The ultra-smart TUI installer** (Python + Rich)          |
| `scripts/`            | power-menu, bg-menu, audio-menu, smart-kill, sync-hypr-lua |
| `wallpapers/`         | Miasma wallpaper set                                       |

## The TUI installer (`installer/green-rice-install`)

This is the star of the repo. Run it on any Arch machine and it provisions the whole rice:

```sh
git clone https://github.com/N4P1x/Green-Rice.git
cd Green-Rice
./installer/green-rice-install
```

### What it does (interactive TUI)

1. **Welcome banner** — rendered in Miasma colours with live palette swatches
2. **System detection** — distro, WM, shell, package manager, fonts, sudo
3. **Interactive component selection** — toggle what you want (packages, fonts, dotfiles, Hyprland Lua, Firefox, Obsidian, VS Code, Vencord, Steam, wallpapers, scripts, verify)
4. **Smart backup** — snapshots your existing `~/.config` into a timestamped `tar.zst` _before_ touching anything
5. **Install** — packages (pacman + yay AUR), fonts (user-local, no sudo), build + link dotfiles, app configs
6. **Verify** — per-check pass/fail (hyprland, kitty, waybar, wofi, mako, symlinks, fonts)
7. **Rollback** — `./installer/green-rice-install --rollback` restores the latest backup

### CLI flags

| Flag                  | What it does                                    |
| --------------------- | ----------------------------------------------- |
| `--dry-run`           | Preview every step without making changes       |
| `-y` / `--yes`        | Non-interactive full install (accept defaults)  |
| `--select A B C`      | Install only these component sets               |
| `--skip-packages`     | Skip system package installation                |
| `--skip-fonts`        | Skip font installation                          |
| `--vault PATH`        | Obsidian vault path                             |
| `--rollback [BACKUP]` | Restore configs from a backup (default: latest) |
| `--list-backups`      | List available backups                          |
| `--state`             | Show install-state log (idempotency)            |

### Why it's better than OMARCHY 4.5's installer

| OMARCHY 4.5                | Green-Rice                                       |
| -------------------------- | ------------------------------------------------ |
| Shell-menu installer       | Full **Rich TUI** with colour swatches           |
| Dotbot symlinks            | `build.sh` + `install.sh` + smart linking        |
| No backup before overwrite | **Timestamped smart backups** every run          |
| No rollback                | **One-command `--rollback`**                     |
| Fixed package list         | **Distro-aware** (pacman/apt/dnf/brew + AUR)     |
| One-shot                   | **Idempotent** — re-run safely, skips done steps |
| No verification            | **Per-check pass/fail verify**                   |

## Quick start (manual, without the TUI)

```sh
./build.sh          # render all templates → dist/
./install.sh dry    # preview what would be linked
./install.sh link   # symlink dist/ into ~/.config
# then: reload Hyprland, restart waybar + mako, log out/in for GTK
```

Re-colour the whole system: edit `palette/colors.conf`, then `./build.sh all && ./install.sh link`.

## Manual installs (outside ~/.config)

See the original dotfiles README — Firefox `userChrome.css`, Obsidian `miasma.css` snippet, VS Code `miasma-color-theme`, Vencord Discord theme, Steam Adwaita CSS, cava, wallpapers via hyprpaper.

## Requirements

- Arch Linux (best experience) — `pacman`, optional `yay`/`paru` for AUR
- Hyprland ≥ 0.56 (Lua config preferred)
- `python3` + `rich` (the TUI installer)
- `git`, `curl`, `unzip`, `zstd`, `fc-cache`

## License

MIT — see [LICENSE](LICENSE).

---

_Green-Rice — because your desktop should install itself._
