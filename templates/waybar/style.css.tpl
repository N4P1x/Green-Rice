/* ========================================================================== */
/* Miasma waybar — Omarchy style, native modules, native palette */
/* ========================================================================== */

@define-color bg #{{bg}};
@define-color bg-lighter #{{bg_lighter}};
@define-color fg #{{fg}};
@define-color fg-muted #{{fg_muted}};
@define-color fg-dim #{{fg_dim}};
@define-color bright #{{fg_bright}};
@define-color accent #{{accent}};
@define-color accent-dark #{{accent_dark}};
@define-color warn #{{yellow}};
@define-color crit #{{red}};
@define-color ok #{{green}};

/* ========================================================================== */
/* Base */
/* ========================================================================== */
* {
  border: none;
  font-family: 'JetBrainsMono Nerd Font Mono', 'JetBrainsMono Nerd Font', 'Noto Color Emoji', 'Noto Sans', sans-serif;
  font-size: 12px;
  min-height: 0;
}

window#waybar {
  background: transparent;
  color: @fg;
}

/* ========================================================================== */
/* Containers — transparent (no outer box) */
/* ========================================================================== */
.modules-left,
.modules-right,
.modules-center {
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 3px 6px;
}

/* ========================================================================== */
/* Modules — each gets the boxed look */
/* ========================================================================== */
#hyprland-window,
#window,
#tray,
#cpu,
#memory,
#battery,
#network,
#pulseaudio,
#backlight {
  min-width: 12px;
}

/* ========================================================================== */
/* Workspaces — explicit box (works in any container) */
/* ========================================================================== */
#workspaces {
  border: 2px solid @accent;
  background-color: @bg;
  box-shadow: 1px 1px 3px 2px alpha(#000000, 0.8);
  padding: 2px 6px;
  margin: 0 8px 0 0;
}

#workspaces button {
  background-color: transparent;
  color: @fg-dim;
  transition: all 0.2s ease-in-out;
  font-size: 11px;
  font-weight: 700;
  padding: 1px 6px;
  margin: 0 1px;
  border-radius: 0;
  min-width: 20px;
}

#workspaces button.active {
  color: @bg;
  background-color: @accent;
  box-shadow: 0 0 8px alpha(@accent, 0.5);
  min-width: 22px;
}

#workspaces button:hover {
  color: @fg;
  background: alpha(@accent, 0.2);
}

#workspaces button.empty {
  color: alpha(@fg-dim, 0.25);
}

#workspaces button.urgent {
  background-color: @crit;
  color: @bg;
}

/* ========================================================================== */
/* Clock — explicit box (Omarchy style) */
/* ========================================================================== */
#clock {
  border: 2px solid @accent;
  background-color: @bg;
  box-shadow: 1px 1px 3px 2px alpha(#000000, 0.8);
  padding: 3px 10px;
  margin: 0;
  color: @fg;
}

/* ========================================================================== */
/* Window title — subtle */
/* ========================================================================== */
#hyprland-window,
#window {
  border: none;
  background: transparent;
  box-shadow: none;
  color: @bright;
  font-size: 12px;
  border: 2px solid @accent;
  background-color: @bg;
  box-shadow: 1px 1px 3px 2px alpha(#000000, 0.8);
  padding: 3px 9px;
  margin: 0 4px;
  border-radius: 0;
}

window#waybar.empty #hyprland-window,
window#waybar.empty #window {
  border: none;
  background: transparent;
  box-shadow: none;
  padding: 0;
  margin: 0;
  min-width: 0;
}

/* ========================================================================== */
/* Right modules — individual boxes */
/* ========================================================================== */
#backlight,
#network,
#pulseaudio,
#cpu,
#memory,
#battery {
  border: 2px solid @accent;
  background-color: @bg;
  box-shadow: 1px 1px 3px 2px alpha(#000000, 0.8);
  padding: 3px 10px;
  margin: 0 4px;
  color: @fg-muted;
  transition: color 0.15s ease;
}

#backlight:hover,
#network:hover,
#pulseaudio:hover,
#cpu:hover,
#memory:hover,
#battery:hover {
  color: @fg;
}

/* Battery states */
#battery.charging {
  color: @ok;
}
#battery.warning {
  color: @warn;
}
#battery.critical {
  color: @crit;
  font-weight: 700;
}

/* Tray */
#tray {
  margin: 0 4px;
}

/* ========================================================================== */
/* Tooltips */
/* ========================================================================== */
tooltip {
  opacity: 0.95;
  background: @bg;
  font-size: 10px;
  border: 2px solid @accent;
  padding: 4px 8px;
  border-radius: 0;
}
tooltip label {
  color: @fg;
}