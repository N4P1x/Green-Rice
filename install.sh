#!/usr/bin/env bash
# Install generated Miasma configs into your system.
#
#   ./install.sh dry        # show what would be linked (default)
#   ./install.sh link       # symlink each generated file into ~/.config
#   ./install.sh copy       # copy instead of symlink
#
# A fresh build always runs first, so installed files can never go stale.
#
# Apps whose theme files live outside ~/.config (VS Code, Firefox, Obsidian,
# Discord, Steam, cava, wallpapers) are handled manually — see README.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST="$HERE/dist"
CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}"

MODE="${1:-dry}"

# Always render a fresh dist so the manifest reflects palette/colors.conf.
"$HERE/build.sh" all

# manifest lines: <dist path> <target path relative to $CONFIG>
declare -r MANIFEST=(
    "hypr/hyprland.conf      hypr/hyprland.conf"
    "hypr/theme.conf         hypr/theme.conf"
    "hypr/theme.lua          hypr/theme.lua"
    "hypr/hyprlock.conf      hypr/hyprlock.conf"
    "hypr/hyprpaper.conf     hypr/hyprpaper.conf"
    "kitty/miasma.conf       kitty/themes/miasma.conf"
    "waybar/config.jsonc     waybar/config.jsonc"
    "waybar/style.css        waybar/style.css"
    "wofi/style.css          wofi/style.css"
    "wofi/config             wofi/config"
    "mako/config             mako/config"
    "gtk/gtk-3.0/gtk.css     gtk-3.0/gtk.css"
    "gtk/gtk-4.0/gtk.css     gtk-4.0/gtk.css"
    "gtk/gtk-3.0/settings.ini gtk-3.0/settings.ini"
    "gtk/gtk-4.0/settings.ini gtk-4.0/settings.ini"
    "btop/miasma.theme       btop/themes/miasma.theme"
    "kde/kdeglobals            kdeglobals"
)

install_one() {
    local src_rel="$1" dst_rel="$2"
    local src="$DIST/$src_rel" dst="$CONFIG/$dst_rel"
    if [[ ! -e "$src" ]]; then
        echo "SKIP  $src_rel  (not built)"
        return
    fi
    mkdir -p "$(dirname "$dst")"
    case "$MODE" in
        link) ln -sfn "$src" "$dst"; echo "LINK  $dst -> $src" ;;
        copy) cp -f  "$src" "$dst"; echo "COPY  $dst" ;;
        dry|*)
            echo "WOULD $dst_rel"
            if [[ -e "$dst" || -L "$dst" ]]; then echo "   (overwrites existing: $dst)"; fi ;;
    esac
}

for entry in "${MANIFEST[@]}"; do
    # shellcheck disable=SC2086
    install_one $entry
done

# --- user scripts (installed to ~/.local/bin) --------------------------------
BINDIR="$HOME/.local/bin"
mkdir -p "$BINDIR"
for script in power-menu bg-menu audio-menu smart-kill; do
    src="$HERE/scripts/$script"
    case "$MODE" in
        link) ln -sfn "$src" "$BINDIR/$script"; echo "LINK  $BINDIR/$script -> $src" ;;
        copy) cp -f  "$src" "$BINDIR/$script"; echo "COPY  $BINDIR/$script" ;;
        dry|*) echo "WOULD $BINDIR/$script" ;;
    esac
done

case "$MODE" in
    link|copy) echo "done. now: reload Hyprland, restart waybar/mako, log out & in for GTK.";;
    *) echo "dry-run. run:  ./install.sh link   (or copy)";;
esac
# Ensure Hyprland Lua theme is required (Hyprland >= 0.56 preference)
if [ -f "$CONFIG/hypr/hyprland.lua" ]; then
    if ! grep -q 'require("theme")' "$CONFIG/hypr/hyprland.lua" 2>/dev/null; then
        echo 'require("theme")' >> "$CONFIG/hypr/hyprland.lua"
        echo "  appended require(\"theme\") to $CONFIG/hypr/hyprland.lua"
    fi
fi