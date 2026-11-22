#!/usr/bin/env bash
# Regenerate ~/.config/hypr/hyprland.lua from hyprland.conf (Hyprland >= 0.56 uses Lua).
# Your dotfiles build from templates/hypr/hyprland.conf.tpl -> dist/hypr/hyprland.conf,
# but Hyprland 0.56+ loads hyprland.lua INSTEAD of hyprland.conf when both exist.
# Run this after ./build.sh / editing hyprland.conf, then it reloads Hyprland.
# Requires hyprlang2lua (yay -S hyprlang2lua).
set -euo pipefail
CONF="${XDG_CONFIG_HOME:-$HOME/.config}/hypr/hyprland.conf"
LUA="${XDG_CONFIG_HOME:-$HOME/.config}/hypr/hyprland.lua"
CONV_BIN=""
for c in /usr/bin/hyprlang2lua /tmp/hyprconv/usr/bin/hyprlang2lua "$HOME/.local/bin/hyprlang2lua"; do
  [[ -x "$c" ]] && CONV_BIN="$c" && break
done
if [[ -z "$CONV_BIN" ]]; then
  echo "error: hyprlang2lua not found. Install: yay -S hyprlang2lua" >&2
  exit 1
fi
TMP="$(mktemp --suffix=.lua)"
"$CONV_BIN" --report "$CONF" -o "$TMP"
python3 - "$TMP" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
s = s.replace(
'''hl.layer_rule({
    match = { namespace = "match:namespace wofi" },
    -- TODO: manual review — unmapped layer rule: "blur on"
})''',
'''hl.layer_rule({
    name = "blur-wofi",
    match = { namespace = "wofi" },
    blur = true,
})''')
s = s.replace(
'''hl.layer_rule({
    match = { namespace = "match:namespace waybar" },
    ignore_alpha = 0,
})''',
'''hl.layer_rule({
    name = "waybar-ignore-alpha",
    match = { namespace = "waybar" },
    ignore_alpha = 0,
})''')
s = s.replace(
'''hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag())
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize())''',
'''hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })''')
if 'require("theme")' not in s:
    s += '\nrequire("theme")\n'
open(p, "w").write(s)
PY
cp -f "$TMP" "$LUA"
echo "installed $LUA"
Hyprland --verify-config --config "$LUA" 2>&1 | tail -n 5
SIG="$(hyprctl instances -j 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d[0].get("instance") or d[0].get("signature") or "" if d else "")')"
if [[ -n "$SIG" ]]; then
  hyprctl --instance "$SIG" reload
  echo "reloaded. binds: $(hyprctl --instance "$SIG" binds -j 2>/dev/null | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')"
else
  echo "Hyprland not running? Log out/in to apply."
fi
