/* Miasma Firefox userChrome.css - generated from palette/colors.conf */
@namespace url("http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul");

/* Page background */
#main-content {
    background: rgb({{dec:bg}}) !important;
}

/* Inactive tabs (pill is .tab-background in modern Firefox) */
.tabbrowser-tab:not([selected]) .tab-background {
    background: rgb({{dec:bg_dark}}) !important;
}
.tabbrowser-tab:not([selected]) .tab-label {
    color: rgb({{dec:fg}}) !important;
}

/* Selected tab */
.tabbrowser-tab[selected] .tab-background {
    background: rgb({{dec:accent}}) !important;
}
.tabbrowser-tab[selected] .tab-label {
    color: rgb({{dec:fg_bright}}) !important;
}

/* Tab hover */
.tabbrowser-tab:hover:not([selected]) .tab-background {
    background: rgb({{dec:bg_lighter}}) !important;
}
.tabbrowser-tab:hover:not([selected]) .tab-label {
    color: rgb({{dec:fg_muted}}) !important;
}

/* System UI colors */
#nav-bar {
    background: rgb({{dec:bg_panel}}) !important;
    border-color: rgb({{dec:accent}}) !important;
}

/* Highlighted text */
::-moz-selection {
    background: rgb({{dec:highlight}}) !important;
    color: rgb({{dec:highlight_fg}}) !important;
}