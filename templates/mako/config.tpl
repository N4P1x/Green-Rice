# Miasma mako notifications — sharp boxes to match waybar/wofi.

text-color=#{{fg}}
border-color=#{{accent}}
background-color=#{{bg}}
progress-color=#{{accent}}
width=420
height=150
padding=12
margin=8
border-size=2
border-radius=0
font=JetBrainsMono Nerd Font Mono 11
markup=1
actions=1
icons=1
max-icon-size=48
icon-border-radius=0
anchor=top-right
outer-margin=20
layer=overlay
sort=-time
max-visible=5
history=1
default-timeout=5000
format=<b>%s</b>\n%b

[urgency=low]
border-color=#{{fg_dim}}
default-timeout=3000

[urgency=normal]
border-color=#{{accent}}
default-timeout=5000

[urgency=critical]
border-color=#{{red}}
text-color=#{{fg_bright}}
default-timeout=0

[app-name=Spotify]
invisible=1

[mode=do-not-disturb]
invisible=true

[mode=do-not-disturb app-name=notify-send]
invisible=false