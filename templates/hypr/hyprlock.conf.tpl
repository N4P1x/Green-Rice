# hyprlock — miasma themed lock screen
# Deliberately minimal & robust:
#   - solid color background (no image path -> avoids hyprlock's image-path crash)
#   - no blur (avoids the gallium/async-render race observed on this machine)
#   - sharp (rounding=0) to match the miasma theme
#   - all colors sourced from palette/colors.conf via {{dec:variable}} references
#   - clock and date removed for minimalist display
#   - greeting text removed for bare minimal display
general {
    ignore_empty_input = true
    immediate_render = false
}

# Solid miasma background — the single most stable render path.
# Color: {{dec:bg_darker}} = deepest scrim/shadow layer (0x101010)
background {
    monitor =
    color = rgba({{dec:bg_darker}}, 1)
}

# Centered sharp password field — matches miasma theme
# Colors sourced from miasma palette:
#   {{dec:accent}} = olive (0x78824b) — interactive accent
#   {{dec:bg_dark}} = 0x151515 — tooltip/locked surfaces
#   {{dec:fg}} = primary foreground (0xc2c2b0)
#   {{dec:red}} = accent red (0x685742) — used for fail_color
#   {{dec:yellow}} = 0xb36d43 — capslock state indicator
input-field {
    monitor =
    size = 340, 58
    outline_thickness = 2
    rounding = 0
    dots_size = 0.22
    dots_spacing = 0.4
    dots_center = true
    # outer border: accent at 70% opacity
    outer_color = rgba({{dec:accent}}, 0.7)
    # inner background: bg_dark at 90% opacity
    inner_color = rgba({{dec:bg_dark}}, 0.9)
    # font color: primary foreground at full opacity
    font_color = rgba({{dec:fg}}, 1)
    font_family = JetBrainsMono Nerd Font
    placeholder_text = <i>Enter password</i>
    # check color: accent at full opacity (for correct input state)
    check_color = rgba({{dec:accent}}, 1)
    # fail color: theme red (0x685742) for incorrect attempts
    fail_color = rgba({{dec:red}}, 1)
    # capslock color: theme yellow (0xb36d43) when Caps Lock is on
    capslock_color = rgba({{dec:yellow}}, 1)
    fail_text = <i><b>$FAIL</b></i>
    position = 0, -75
    halign = center
    valign = center
}
