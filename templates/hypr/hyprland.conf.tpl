# Hyprland main configuration.
# THEME (colors, blur, animations) lives in theme.conf — edit palette and re-run ./build.sh.
# This file is yours: bindings, wallpaper, autostart, monitors.

source = ~/.config/hypr/theme.conf

monitor = ,preferred,auto,1

# ---- environment -----------------------------------------------------------
# Qt apps (Dolphin) follow the Miasma GTK theme via the gtk3 platform plugin.
env = QT_QPA_PLATFORMTHEME,gtk3
# Intel HD 520 (Skylake): force modern media driver for HW video decode,
# Electron Wayland-native (Discord/Code/Obsidian), Firefox Wayland.
env = LIBVA_DRIVER_NAME,iHD
env = ELECTRON_OZONE_PLATFORM_HINT,auto
env = MOZ_ENABLE_WAYLAND,1

# ---- variables -----------------------------------------------------------
# Single place to swap apps. All bindings below use these.
$terminal = kitty
$menu     = wofi --show drun --prompt Apps
$browser  = firefox
$files    = dolphin
$editor   = code
$notes    = obsidian
$nnote    = kwrite
$lock     = hyprlock
$power    = {{HOME}}/.local/bin/power-menu
$wall     = {{HOME}}/.local/bin/bg-menu
$audio    = {{HOME}}/.local/bin/audio-menu
$kill     = {{HOME}}/.local/bin/smart-kill
$shots    = {{HOME}}/Pictures/Screenshots

# ---- autostart -----------------------------------------------------------
exec-once = waybar
exec-once = mako
exec-once = hyprpaper
# polkit agent: kde agent is what is installed on this system
# (was polkit-gnome path which does not exist -> auth dialogs never appeared)
exec-once = /usr/lib/polkit-kde-authentication-agent-1

# ---- input ---------------------------------------------------------------
input {
    kb_layout = us
    follow_mouse = 1
    touchpad {
        natural_scroll = false
    }
}

# ---- general -------------------------------------------------------------
general {
    gaps_in = 4
    gaps_out = 8
    border_size = 2
    layout = dwindle
}

cursor {
    # Intel HD 520 supports HW cursors — false saves CPU vs software compositing.
    # If cursor ever goes invisible, flip back to true.
    no_hardware_cursors = false
}

misc {
    disable_hyprland_logo = true
    focus_on_activate = true
    # so bg-menu wallpaper swaps don't flash the anime mask
    force_default_wallpaper = 1
}

dwindle {
    preserve_split = true
}

binds {
    # allow Super+arrows/HJKL focus to work in more situations
    focus_preferred_method = 0
}

# float small dialogs, keep tiling clean
# (0.55+ syntax: windowrule with match: + explicit on/off — windowrulev2 is dead)
windowrule = float on, match:class ^(pavucontrol)$
windowrule = float on, match:class ^(nm-connection-editor)$
windowrule = float on, match:title ^(nmtui)$
windowrule = float on, match:title ^(mixer)$
windowrule = float on, match:title ^(btop)$
windowrule = float on, match:title ^(pacsea)$
windowrule = pin on, match:class ^(hyprland-preview-share-picker)$
# perf: opaque heavy apps skip blur — big GPU saver on HD 520
windowrule = noblur on, match:class ^(discord|vesktop|Code|code|firefox|helium|helium-browser|obsidian|onlyoffice-desktopeditors)$
# wofi + waybar live in the overlay layer
layerrule = blur on, match:namespace wofi
layerrule = ignore_alpha 0, match:namespace waybar

# ---- keybindings ----------------------------------------------------------
# CHEATSHEET (Super = $mainMod)
#  Launch:  T term | A app menu | B browser | E files
#           C vscode | O obsidian | N quick note | P pacsea | Shift+T floating term | W wallpaper | Esc power | Shift+N network
#  Window:  Q kill | F fullscreen | V float | Shift+P pin | Shift+C center
#           Shift+J split | Y group | Tab group-next
#  Focus:   HJK / arrows (L = lock) | Move: Alt+HJKL / arrows | Resize: Ctrl+HJKL / arrows
#  Work:    1-0 switch | Shift+1-0 move | S scratchpad | , . next/prev
#  System:  Shift+Q exit | Shift+R reload | L lock | Shift+Z suspend
#  Shots:   Print region | Shift+Print full | Mod+G full | Mod+Shift+G region
#  Media:   XF86 volume/brightness/mic/player (repeat + works locked)

$mainMod = SUPER

# ---- launch --------------------------------------------------------------
bind = $mainMod, A, exec, $menu
bind = $mainMod, B, exec, $browser
bind = $mainMod, E, exec, $files
bind = $mainMod, C, exec, $editor
bind = $mainMod, O, exec, $notes
bind = $mainMod, T, exec, $terminal
bind = $mainMod SHIFT, T, exec, $terminal --class float-term
bind = $mainMod, W, exec, $wall
bind = $mainMod, Escape, exec, $power
bind = $mainMod, N, exec, $nnote
bind = $mainMod SHIFT, N, exec, $terminal --title nmtui -e nmtui
bind = $mainMod, P, exec, $terminal --title pacsea -e pacsea
# audio menu (wpctl + wofi, no extra deps)
bind = $mainMod, M, exec, $audio

# ---- window actions --------------------------------------------------------
# Super+Q: smart-kill — Discord/tray apps get SIGKILL'd (actually quit),
# everything else gets a graceful close.
bind = $mainMod, Q, exec, $kill
bind = $mainMod, F, fullscreen, 0
bind = $mainMod, V, togglefloating
bind = $mainMod SHIFT, P, pin
bind = $mainMod SHIFT, C, centerwindow
bind = $mainMod SHIFT, J, layoutmsg, togglesplit
bind = $mainMod, Y, togglegroup
bind = $mainMod SHIFT, Y, moveoutofgroup
bind = $mainMod, Tab, changegroupactive, f
bind = $mainMod SHIFT, Tab, changegroupactive, b
bind = $mainMod, U, pseudo

# ---- focus (Mod + HJKL / arrows) -------------------------------------------
bind = $mainMod, H, movefocus, l
bind = $mainMod, J, movefocus, d
bind = $mainMod, K, movefocus, u
# NOTE: Super+L is lock. Focus-right is arrows / Alt / Ctrl combos below.
bind = $mainMod, left, movefocus, l
bind = $mainMod, down, movefocus, d
bind = $mainMod, up, movefocus, u
bind = $mainMod, right, movefocus, r

# ---- move window (Mod+Alt + HJKL / arrows) ----------------------------------
bind = $mainMod ALT, H, movewindow, l
bind = $mainMod ALT, J, movewindow, d
bind = $mainMod ALT, K, movewindow, u
bind = $mainMod ALT, L, movewindow, r
bind = $mainMod ALT, left, movewindow, l
bind = $mainMod ALT, down, movewindow, d
bind = $mainMod ALT, up, movewindow, u
bind = $mainMod ALT, right, movewindow, r

# ---- resize (Mod+Ctrl + HJKL / arrows, repeatable) ---------------------------
binde = $mainMod CTRL, H, resizeactive, -20 0
binde = $mainMod CTRL, J, resizeactive, 0 20
binde = $mainMod CTRL, K, resizeactive, 0 -20
binde = $mainMod CTRL, L, resizeactive, 20 0
binde = $mainMod CTRL, left, resizeactive, -20 0
binde = $mainMod CTRL, down, resizeactive, 0 20
binde = $mainMod CTRL, up, resizeactive, 0 -20
binde = $mainMod CTRL, right, resizeactive, 20 0

bindm = $mainMod, mouse:272, movewindow
bindm = $mainMod, mouse:273, resizewindow

# ---- workspaces --------------------------------------------------------------
bind = $mainMod, 1, workspace, 1
bind = $mainMod, 2, workspace, 2
bind = $mainMod, 3, workspace, 3
bind = $mainMod, 4, workspace, 4
bind = $mainMod, 5, workspace, 5
bind = $mainMod, 6, workspace, 6
bind = $mainMod, 7, workspace, 7
bind = $mainMod, 8, workspace, 8
bind = $mainMod, 9, workspace, 9
bind = $mainMod, 0, workspace, 10

bind = $mainMod SHIFT, 1, movetoworkspace, 1
bind = $mainMod SHIFT, 2, movetoworkspace, 2
bind = $mainMod SHIFT, 3, movetoworkspace, 3
bind = $mainMod SHIFT, 4, movetoworkspace, 4
bind = $mainMod SHIFT, 5, movetoworkspace, 5
bind = $mainMod SHIFT, 6, movetoworkspace, 6
bind = $mainMod SHIFT, 7, movetoworkspace, 7
bind = $mainMod SHIFT, 8, movetoworkspace, 8
bind = $mainMod SHIFT, 9, movetoworkspace, 9
bind = $mainMod SHIFT, 0, movetoworkspace, 10

# next / prev workspace (Tab pair already used for groups, so use . ,)
bind = $mainMod, period, workspace, e+1
bind = $mainMod, comma, workspace, e-1
bind = $mainMod SHIFT, period, movetoworkspace, e+1
bind = $mainMod SHIFT, comma, movetoworkspace, e-1

# scratchpad
bind = $mainMod, S, togglespecialworkspace
bind = $mainMod SHIFT, S, movetoworkspace, special

# monitor move (focus.bind dropped: Super+O is obsidian; no-op on single monitor anyway)
bind = $mainMod SHIFT, O, movecurrentworkspacetomonitor, +1

# ---- system ------------------------------------------------------------------
bind = $mainMod SHIFT, Q, exit
bind = $mainMod SHIFT, R, exec, hyprctl reload
bind = $mainMod, L, exec, $lock
bind = $mainMod SHIFT, Z, exec, systemctl suspend
bind = $mainMod, F12, exec, $terminal --title btop -e btop
bind = $mainMod SHIFT, F12, exec, $terminal --title htop -e htop
# restart bar / notifier without logging out
bind = $mainMod SHIFT, W, exec, sh -c 'pkill waybar; sleep 0.2; waybar &'
bind = $mainMod SHIFT, M, exec, sh -c 'pkill mako; sleep 0.2; mako &'

# ---- screenshots (file-first, clipboard-if-available) --------------------------
# Saves to $shots with timestamp. Tries wl-copy when wl-clipboard is
# installed, notifies via dunstify (installed) — no hard deps.
# NOTE: no shell $vars here on purpose — Hyprland would eat $f as its own
# variable. $shots is a Hyprland var (expands fine); $(...) is left alone.
# Install for full behavior: sudo pacman -S wl-clipboard libnotify
bind = , Print, exec, sh -c 'mkdir -p $shots; grim -g "$(slurp)" $shots/$(date +%Y-%m-%d_%H-%M-%S).png; dunstify "Screenshot saved" 2>/dev/null || true'
bind = SHIFT, Print, exec, sh -c 'mkdir -p $shots; grim $shots/$(date +%Y-%m-%d_%H-%M-%S-full).png; dunstify "Screenshot saved" 2>/dev/null || true'
bind = $mainMod, G, exec, sh -c 'mkdir -p $shots; grim $shots/$(date +%Y-%m-%d_%H-%M-%S-full).png; dunstify "Screenshot saved" 2>/dev/null || true'
bind = $mainMod SHIFT, G, exec, sh -c 'mkdir -p $shots; grim -g "$(slurp)" $shots/$(date +%Y-%m-%d_%H-%M-%S).png; dunstify "Screenshot saved" 2>/dev/null || true'

# ---- media keys (bindle = repeat + works locked) --------------------------------
bindle = , XF86AudioLowerVolume, exec, wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
bindle = , XF86AudioRaiseVolume, exec, wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+
bindl = , XF86AudioMute, exec, wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
bindl = , XF86AudioMicMute, exec, wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle
bindl = , XF86AudioPlay, exec, playerctl play-pause
bindl = , XF86AudioNext, exec, playerctl next
bindl = , XF86AudioPrev, exec, playerctl previous
bindl = , XF86AudioStop, exec, playerctl stop
# brightness: whatever is installed wins. intel_backlight exists in /sys.
# Install for full behavior: sudo pacman -S brightnessctl
bindle = , XF86MonBrightnessUp, exec, sh -c 'brightnessctl set +5% 2>/dev/null || light -A 5 2>/dev/null || brillo -A 5 2>/dev/null || dunstify "Brightness" "install brightnessctl" 2>/dev/null || true'
bindle = , XF86MonBrightnessDown, exec, sh -c 'brightnessctl set 5%- 2>/dev/null || light -U 5 2>/dev/null || brillo -U 5 2>/dev/null || dunstify "Brightness" "install brightnessctl" 2>/dev/null || true'
