# Miasma theme — borders, decorations, animations.
# Sourced from hyprland.conf. Regenerate with ./build.sh and reload Hyprland.

general {
    col.active_border = rgb({{accent}}) rgb({{accent_dark}}) {{border_angle}}deg
    col.inactive_border = rgb({{accent_mid}}) rgb({{bg}}) {{border_angle}}deg
}

group {
    col.border_active = rgb({{accent}}) rgb({{accent_dark}}) {{border_angle}}deg
    col.border_inactive = rgb({{accent_mid}}) rgb({{bg}}) {{border_angle}}deg
}

decoration {
    dim_strength = 0.12

    blur {
        enabled = true
        size = 6
        passes = 1
    }

    shadow {
        enabled = true
        range = 8
        render_power = 2
        color = rgba({{black}}99)
        offset = 2 2
    }
}

animations {
    enabled = yes

    bezier = miasma,  0.55, 0.02, 0.38, 0.98
    bezier = fogbank, 0.70, 0.01, 0.30, 1.00
    bezier = toxic,   0.85, 0.00, 0.25, 1.00

    animation = windows,     1, 4, miasma
    animation = windowsIn,   0,  0, default
    animation = windowsOut,  0,  0, default
    animation = windowsMove, 1,  3, miasma
    animation = fade,        1, 4, fogbank
    animation = fadeIn,      1, 4, fogbank
    animation = fadeOut,     1, 3, fogbank
    animation = workspaces,  1, 3, fogbank, fade
}