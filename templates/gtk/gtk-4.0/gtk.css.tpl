/* Miasma GTK4 / libadwaita override. Ships as ~/.config/gtk-4.0/gtk.css. */

@define-color background #{{bg}};
@define-color foreground #{{fg}};

@define-color accent #{{accent}};
@define-color red #{{red}};
@define-color green #{{green}};
@define-color yellow #{{yellow}};
@define-color magenta #{{magenta}};
@define-color cyan #{{cyan}};
@define-color bright_black #{{bright_black}};
@define-color dim #{{fg_dim}};
@define-color selection_bg #{{highlight}};
@define-color selection_fg #{{highlight_fg}};

@define-color accent_bg_color @accent;
@define-color accent_fg_color @background;
@define-color accent_color @cyan;

@define-color window_bg_color @background;
@define-color window_fg_color @foreground;

@define-color view_bg_color @background;
@define-color view_fg_color @foreground;
@define-color headerbar_bg_color @background;
@define-color headerbar_fg_color @foreground;
@define-color popover_bg_color @background;
@define-color popover_fg_color @foreground;
@define-color card_bg_color @background;
@define-color card_fg_color @foreground;
@define-color dialog_bg_color @background;
@define-color dialog_fg_color @foreground;

@define-color destructive_bg_color @red;
@define-color destructive_fg_color @foreground;
@define-color success_bg_color @green;
@define-color success_fg_color @background;
@define-color warning_bg_color @yellow;
@define-color warning_fg_color @background;
@define-color error_bg_color @red;
@define-color error_fg_color @foreground;

@define-color borders alpha(@foreground, 0.1);

* {
    border-radius: 0;
}