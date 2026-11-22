---@module "hyprland"
---@diagnostic disable: undefined-global

-- Miasma theme for Hyprland's Lua config (Hyprland >= 0.56).
-- require("theme") from inside hyprland.lua, after your other settings.

hl.config({
    general = {
        col = {
            active_border   = { colors = { "rgb({{dec:accent}})", "rgb({{dec:accent_dark}})" }, angle = 35 },
            inactive_border = { colors = { "rgb({{dec:accent_mid}})", "rgb({{dec:bg}})" }, angle = 35 },
        },
    },

    decoration = {
        dim_strength = 0.12,

        shadow = {
            enabled      = true,
            range        = 8,
            render_power = 2,
            color        = 0x99000000,
        },

        blur = {
            enabled = true,
            size    = 6,
            passes  = 1,
        },
    },

    animations = { enabled = true },
})

-- Miasma curves + motion (mirror of theme.conf, lua API form)
hl.curve("miasma",  { type = "bezier", points = { {0.55, 0.02}, {0.38, 0.98} } })
hl.curve("fogbank", { type = "bezier", points = { {0.70, 0.01}, {0.30, 1.00} } })
hl.curve("toxic",   { type = "bezier", points = { {0.85, 0.00}, {0.25, 1.00} } })

hl.animation({ leaf = "windows",       enabled = true, speed = 4, bezier = "miasma" })
hl.animation({ leaf = "windowsIn",     enabled = false })
hl.animation({ leaf = "windowsOut",    enabled = false })
hl.animation({ leaf = "windowsMove",   enabled = true, speed = 3, bezier = "miasma" })
hl.animation({ leaf = "fade",          enabled = true, speed = 4, bezier = "fogbank" })
hl.animation({ leaf = "fadeIn",        enabled = true, speed = 4, bezier = "fogbank" })
hl.animation({ leaf = "fadeOut",       enabled = true, speed = 3, bezier = "fogbank" })
hl.animation({ leaf = "workspaces",    enabled = true, speed = 3, bezier = "fogbank", style = "fade" })