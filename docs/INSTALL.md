# Green-Rice install guide

The **Miasma** Hyprland rice, provisioned by an ultra-smart TUI installer.

## Option 1 — TUI installer (recommended)

```sh
git clone https://github.com/N4P1x/Green-Rice.git
cd Green-Rice
./installer/green-rice-install
```

The TUI walks you through:

1. System detection (distro, WM, package manager, fonts, sudo)
2. Miasma palette preview (live colour swatches)
3. Interactive component selection (toggle what you want)
4. Smart backup of existing `~/.config` (timestamped tar.zst)
5. Install: packages → fonts → dotfiles → apps → verify
6. Post-install verification (pass/fail per check)

After it finishes: **log out and back in** so Hyprland + GTK pick up the new configs.

### Common invocations

```sh
./installer/green-rice-install          # interactive TUI
./installer/green-rice-install --dry-run # preview, zero changes
./installer/green-rice-install -y        # non-interactive full install
./installer/green-rice-install --select dotfiles fonts verify   # only these
./installer/green-rice-install --rollback        # restore latest backup
./installer/green-rice-install --list-backups    # list backups
./installer/green-rice-install --state           # idempotency log
```

## Option 2 — manual (build.sh + install.sh)

```sh
./build.sh          # render templates → dist/  (or ./build.sh hypr, ./build.sh bar, …)
./install.sh dry    # preview symlinks
./install.sh link   # symlink dist/ into ~/.config
./install.sh copy   # copy instead of symlink
```

Then reload Hyprland, restart waybar + mako, and log out/in for GTK.

## Component sets

| Set        | Installs                                                                              |
| ---------- | ------------------------------------------------------------------------------------- |
| packages   | hyprland, kitty, waybar, wofi, mako, firefox, obsidian, code, btop, fonts, … (pacman) |
| fonts      | JetBrainsMono Nerd Font + Noto Color Emoji (user-local, no sudo)                      |
| dotfiles   | all Miasma configs built + linked into ~/.config                                      |
| hypr-lua   | Hyprland Lua theme + live keybinding sync                                             |
| firefox    | userChrome.css + dark-theme prefs                                                     |
| obsidian   | miasma.css snippet (needs a vault)                                                    |
| vscode     | Miasma colour theme                                                                   |
| vencord    | Discord theme (load manually in Vencord)                                              |
| steam      | Adwaita CSS (apply manually in Steam)                                                 |
| wallpapers | Miasma wallpaper set                                                                  |
| scripts    | power-menu, bg-menu, audio-menu, smart-kill → ~/.local/bin                            |
| verify     | post-install pass/fail checks                                                         |

## Rollback

Backups live in `~/.local/state/green-rice/backups/`. To restore the latest:

```sh
./installer/green-rice-install --rollback
```

Or restore a specific backup:

```sh
./installer/green-rice-install --rollback green-rice-backup-pre-install-20261122-1953.tar.zst
```

## Idempotency

The installer records what it did in `~/.local/state/green-rice/state.json`. Re-running is safe — already-done steps are skipped.

## Requirements

- Arch Linux (best), `pacman` (+ `yay`/`paru` for AUR packages like `hyprlang2lua`)
- Hyprland ≥ 0.56
- `python3` and the `rich` package (TUI installer)
- `git`, `curl`, `unzip`, `zstd`, `fc-cache`
