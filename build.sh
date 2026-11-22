#!/usr/bin/env bash
# Miasma rice build script.
# Reads palette/colors.conf, renders templates/ -> dist/.
# Usage: ./build.sh            # render everything into dist/
#        ./build.sh <set>      # e.g. ./build.sh hypr  (see SETS below)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PALETTE="$HERE/palette/colors.conf"
TEMPLATES="$HERE/templates"
DIST="$HERE/dist"

# --- load palette ----------------------------------------------------------
declare -A C
while read -r k v _; do
    [[ -z "$k" || "$k" == \#* ]] && continue
    C["$k"]="$v"
done < "$PALETTE"

# --- sed args: {{key}} -> hex, {{dec:key}} -> "R, G, B" ----------------------
patterns=(-e "s|{{HOME}}|$HOME|g")
for k in "${!C[@]}"; do
    v="${C[$k]}"
    patterns+=(-e "s|{{$k}}|$v|g")
    if [[ "$v" =~ ^[0-9a-fA-F]{6}$ ]]; then
        r=$((16#${v:0:2})); g=$((16#${v:2:2})); b=$((16#${v:4:2}))
        # No spaces: Hyprland's gradient parser splits on spaces, so
        # "rgb(120, 130, 75)" breaks but "rgb(120,130,75)" parses.
        # (CSS rgb() accepts both, so this is safe everywhere.)
        patterns+=(-e "s|{{dec:$k}}|$r,$g,$b|g")
    fi
done

# --- render ----------------------------------------------------------------
# render <template> <output> [header]   header in {hash,css,slash,lua,none}
render() {
    local src="$1" dst="$2" style="${3:-hash}"
    mkdir -p "$(dirname "$dst")"
    : > "$dst"
    case "$style" in
        hash)  printf '# GENERATED: %s  |  palette/colors.conf  |  template: %s\n# Do not edit; change the template and re-run ./build.sh\n\n' "$dst" "${src#"$TEMPLATES"/}" > "$dst" ;;
        css)  printf '/* GENERATED: %s  |  palette/colors.conf  |  template: %s */\n/* Do not edit; change the template and re-run ./build.sh */\n\n' "$dst" "${src#"$TEMPLATES"/}" > "$dst" ;;
        slash) printf '// GENERATED: %s  |  palette/colors.conf  |  template: %s\n// Do not edit; change the template and re-run ./build.sh\n\n' "$dst" "${src#"$TEMPLATES"/}" > "$dst" ;;
        lua)  printf -- '-- GENERATED: %s  |  palette/colors.conf  |  template: %s\n-- Do not edit; change the template and re-run ./build.sh\n\n' "$dst" "${src#"$TEMPLATES"/}" > "$dst" ;;
        none)  : ;;
    esac
    sed "${patterns[@]}" "$src" >> "$dst"
}

# --- sets -------------------------------------------------------------------
build_hypr() {
    render "$TEMPLATES/hypr/hyprland.conf.tpl"     "$DIST/hypr/hyprland.conf"
    render "$TEMPLATES/hypr/theme.conf.tpl"        "$DIST/hypr/theme.conf"
    render "$TEMPLATES/hypr/hyprlock.conf.tpl"     "$DIST/hypr/hyprlock.conf"
    render "$TEMPLATES/hypr/hyprpaper.conf.tpl"    "$DIST/hypr/hyprpaper.conf"
    render "$TEMPLATES/hypr/hyprland-preview-share-picker.css.tpl" "$DIST/hypr/hyprland-preview-share-picker.css" css
    render "$TEMPLATES/hypr/theme.lua.tpl" "$DIST/hypr/theme.lua" lua
}

build_terminal() {
    render "$TEMPLATES/kitty/miasma.conf.tpl"      "$DIST/kitty/miasma.conf"
}

build_bar() {
    render "$TEMPLATES/waybar/config.jsonc.tpl"    "$DIST/waybar/config.jsonc" slash
    render "$TEMPLATES/waybar/style.css.tpl"       "$DIST/waybar/style.css"    css
}

build_launcher() {
    render "$TEMPLATES/wofi/style.css.tpl"         "$DIST/wofi/style.css"      css
    render "$TEMPLATES/wofi/config.tpl"            "$DIST/wofi/config"         none
}

build_notify() {
    render "$TEMPLATES/mako/config.tpl"            "$DIST/mako/config"
}

build_gtk() {
    render "$TEMPLATES/gtk/gtk-3.0/gtk.css.tpl"    "$DIST/gtk/gtk-3.0/gtk.css" css
    render "$TEMPLATES/gtk/gtk-4.0/gtk.css.tpl"    "$DIST/gtk/gtk-4.0/gtk.css" css
    render "$TEMPLATES/gtk/settings/settings.ini.tpl" "$DIST/gtk/gtk-3.0/settings.ini"
    render "$TEMPLATES/gtk/settings/settings.ini.tpl" "$DIST/gtk/gtk-4.0/settings.ini" hash
}

build_cli() {
    render "$TEMPLATES/btop/miasma.theme.tpl"      "$DIST/btop/miasma.theme"
    render "$TEMPLATES/cava/miasma.conf.tpl"       "$DIST/cava/miasma.conf"
}

build_kde() {
    render "$TEMPLATES/kde/kdeglobals.tpl"         "$DIST/kde/kdeglobals"
}

build_apps() {
    render "$TEMPLATES/obsidian/miasma.css.tpl"    "$DIST/obsidian/miasma.css"            css
    render "$TEMPLATES/firefox/userChrome.css.tpl" "$DIST/firefox/userChrome.css"         css
    render "$TEMPLATES/vencord/miasma.theme.css.tpl" "$DIST/vencord/miasma.theme.css"     css
    render "$TEMPLATES/steam/steam.css.tpl"        "$DIST/steam/steam.css"                css
    mkdir -p "$DIST/chromium/miasma-theme"
    cp -f "$TEMPLATES/chromium/miasma-theme/manifest.json" "$DIST/chromium/miasma-theme/manifest.json"
}

build_editor() {
    render "$TEMPLATES/vscode/miasma.theme.json.tpl" "$DIST/vscode/themes/miasma-color-theme.json" none
    render "$TEMPLATES/vscode/package.json.tpl"      "$DIST/vscode/package.json"                  none
}

build_all() {
    build_hypr
    build_terminal
    build_bar
    build_launcher
    build_notify
    build_gtk
    build_cli
    build_kde
    build_apps
    build_editor
}

# --- dispatch ----------------------------------------------------------------
SETS=(hypr terminal bar launcher notify gtk cli kde apps editor all)
target="${1:-all}"

case "$target" in
    all)      build_all ;;
    hypr)     build_hypr ;;
    terminal) build_terminal ;;
    bar)      build_bar ;;
    launcher) build_launcher ;;
    notify)   build_notify ;;
    gtk)      build_gtk ;;
    cli)      build_cli ;;
    kde)      build_kde ;;
    apps)     build_apps ;;
    editor)   build_editor ;;
    *)
        echo "usage: $0 [${SETS[*]}]" >&2
        exit 1 ;;
esac

echo "built '$target' into $DIST"