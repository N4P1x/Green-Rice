{
  "reload_style_on_change": true,
  "layer": "top",
  "position": "top",
  "spacing": 0,
  "height": 33,
  "margin": "0",
  "modules-left": [
    "ext/workspaces",
    "hyprland/window"
  ],
  "modules-center": [
    "clock"
  ],
  "modules-right": [
    "backlight",
    "pulseaudio",
    "cpu",
    "memory",
    "network",
    "battery"
  ],
  "ext/workspaces": {
    "format": "{icon}",
    "format-icons": {
      "default": "",
      "1": "1",
      "2": "2",
      "3": "3",
      "4": "4",
      "5": "5",
      "6": "6",
      "7": "7",
      "8": "8",
      "9": "9"
    },
    "on-click": "activate",
    "all-outputs": true,
    "tooltip-format": "Workspace {id}"
  },
  "hyprland/window": {
    "format": "{title}",
    "max-length": 25,
    "rewrite": {
      " - ": "",
      "(.*?) - Chromium - chromium": "  $1 ",
      "(.*chrome)...(.*)": "  $1 ",
      "(.*) - Obsidian - .* - obsidian": "  $1 ",
      "(.*nvim)...(.*)": "  $2 ",
      "(.*code) - (.*)": " 󰨞 $1 ",
      "^.*btop( .*|$)": " 󰧨 BTOP $1 ",
      "^.*cmatrix( .*|$)": " 󰘨 MATRIX $1 ",
      "(.*) - Spotify": "  $1 ",
      "(.*) - com.mitchellh.ghostty": " 󰊠 $1 ",
      "(.*) - Alacritty": "   $1 ",
      "(.*) - BeeperTexts": " 󰻞  $1 ",
      "(.*Discord)...(.*).. (.*)": "  $2 ",
      "(.*) - org.gnome.Nautilus": " 󰣆 $1 ",
      "(.*) - fish": "  [$1] ",
      "(.*Steam)...(.*)": "  $1"
    }
  },
  "backlight": {
    "device": "intel_backlight",
    "format": "{percent}% {icon}",
    "format-icons": [
      "󰃚",
      "󰃛",
      "󰃜",
      "󰃝",
      "󰃞"
    ]
  },
  "network": {
    "interface": "wlp3s0",
    "format-icons": [
      "󰤯",
      "󰤟",
      "󰤢",
      "󰤥",
      "󰤨"
    ],
    "format-wifi": "{essid} {icon}",
    "format-ethernet": "󰀂 {ipaddr}",
    "format-disconnected": "󰤮 Offline",
    "tooltip-format-wifi": "{essid} ({frequency} GHz)\n⇣{bandwidthDownBytes}  ⇡{bandwidthUpBytes}",
    "tooltip-format-ethernet": "{ipaddr}\n⇣{bandwidthDownBytes}  ⇡{bandwidthUpBytes}",
    "tooltip-format-disconnected": "Disconnected",
    "interval": 3,
    "on-click": "kitty --title nmtui -e nmtui"
  },
  "battery": {
    "bat": "BAT1",
    "adapter": "AC",
    "format": "{icon} {capacity}%",
    "format-discharging": "{icon} {capacity}%",
    "format-charging": "{icon} {capacity}%",
    "format-plugged": "",
    "format-icons": {
      "charging": [
        "󰢜",
        "󰂆",
        "󰂇",
        "󰂈",
        "󰢝",
        "󰂉",
        "󰢞",
        "󰂊",
        "󰂋",
        "󰂅"
      ],
      "default": [
        "󰁺",
        "󰁻",
        "󰁼",
        "󰁽",
        "󰁾",
        "󰁿",
        "󰂀",
        "󰂁",
        "󰂂",
        "󰁹"
      ]
    },
    "format-full": "󰂅",
    "tooltip-format-discharging": "{power:>1.0f}W↓ {capacity}%",
    "tooltip-format-charging": "{power:>1.0f}W↑ {capacity}%",
    "interval": 5,
    "states": {
      "warning": 20,
      "critical": 10
    }
  },
  "pulseaudio": {
    "format": "{icon} {volume}%",
    "on-click": "{{HOME}}/.local/bin/audio-menu",
    "on-click-right": "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle",
    "tooltip-format": "Playing at {volume}%",
    "scroll-step": 5,
    "format-muted": "󰝟",
    "format-icons": {
      "default": [
        "",
        "",
        ""
      ]
    }
  },
  "cpu": {
    "interval": 2,
    "format": "󰍛 {usage}%",
    "on-click": "kitty --title btop -e btop"
  },
  "memory": {
    "interval": 2,
    "format": "󰾅 {percentage}%",
    "on-click": "kitty --title btop -e btop"
  },
  "clock": {
    "format": "{:%I:%M %p  %a %e }",
    "format-alt": "{:%A %d/%m/%Y}",
    "tooltip-format": "<span>{calendar}</span>",
    "calendar": {
      "mode": "month",
      "mode-mon-col": 3,
      "on-click-right": "mode",
      "format": {
        "month": "<span weight='bold'>{}</span>",
        "weekdays": "<span weight='bold'>{}</span>",
        "today": "<span weight='bold' underline='single'>{}</span>"
      }
    }
  },
  "tray": {
    "icon-size": 12,
    "spacing": 12
  }
}