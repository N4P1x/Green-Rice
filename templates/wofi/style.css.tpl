@define-color bg #{{bg}};
@define-color bg_panel #{{bg_panel}};
@define-color bg_dark #{{bg_dark}};
@define-color fg #{{fg}};
@define-color fg_muted #{{fg_muted}};
@define-color fg_dim #{{fg_dim}};
@define-color accent #{{accent}};

* {
  font-family: 'JetBrainsMono Nerd Font Mono', 'JetBrainsMono Nerd Font', 'Noto Color Emoji', 'Noto Sans', sans-serif;
  border-radius: 0;
}

window {
  background-color: @bg_panel;
  border: 2px solid @accent;
  box-shadow: 1px 1px 3px 2px alpha(#000000, 0.8);
  font-size: 13px;
}

#outer-box {
  padding: 10px;
  background-color: transparent;
}

#input {
  background-color: @bg_dark;
  color: @fg;
  border: 1px solid @fg_dim;
  border-bottom: 2px solid @accent;
  padding: 8px 12px;
  font-size: 13px;
}

#input:focus {
  border-color: @accent;
}

#entry {
  color: @fg_muted;
  background-color: transparent;
  padding: 8px 12px;
  margin: 2px 0;
}

#entry:selected {
  background-color: @accent;
  color: #{{bg}};
  box-shadow: 0 0 8px alpha(@accent, 0.5);
}

#entry:hover:not(:selected) {
  background-color: alpha(@accent, 0.15);
  color: @fg;
}

scrollbar {
  background-color: @bg_panel;
}

scrollbar slider {
  background-color: @fg_dim;
  border-radius: 0;
}

scrollbar slider:hover {
  background-color: @accent;
}