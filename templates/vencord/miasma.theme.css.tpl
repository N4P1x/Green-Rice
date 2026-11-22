/**
 * @name Miasma (Discord)
 * @description Self-contained Miasma theme for Discord. No network imports:
 *   this bundles the base16-discord mapping (bypass_/base16-Discord) that the
 *   original relied on as a hosted @import.
 */

:root {
    --color00: #{{bg}};
    --color01: #{{red}};
    --color02: #{{green}};
    --color03: #{{yellow}};
    --color04: #{{accent}};
    --color05: #{{magenta}};
    --color06: #{{cyan}};
    --color07: #{{fg_bright}};
    --color08: #{{bright_black}};
    --color09: #{{bright_red}};
    --color10: #{{bright_green}};
    --color11: #{{bright_yellow}};
    --color12: #{{bright_blue}};
    --color13: #{{bright_magenta}};
    --color14: #{{bright_cyan}};
    --color15: #{{bright_white}};
}

/* --- base16-discord base mapping (vendored, from imbypass/base16-Discord) --- */

:root {
    --base00: var(--color00);
    --base01: color-mix(in srgb, var(--color00) 100%, white);
    --base02: color-mix(in srgb, var(--color00) 90%, white);
    --base03: color-mix(in srgb, var(--color00) 80%, white);
    --base04: color-mix(in srgb, var(--color00) 70%, white);
    --base05: var(--color05);
    --base06: color-mix(in srgb, var(--color05) 75%, white);
    --base07: color-mix(in srgb, var(--color05) 70%, white);
    --base08: var(--color08);
    --base09: var(--color09);
    --base0A: var(--color10);
    --base0B: var(--color11);
    --base0C: var(--color12);
    --base0D: var(--color13);
    --base0E: var(--color14);
    --base0F: var(--color15);
}

.theme-light,
.theme-dark,
.theme-darker,
.theme-midnight,
.visual-refresh {
    --activity-card-background: var(--base01) !important;
    --background-accent: var(--base03) !important;
    --background-floating: var(--base02) !important;
    --background-mentioned-hover: var(--base03) !important;
    --background-mentioned: var(--base02) !important;
    --background-message-highlight: var(--base02) !important;
    --background-message-hover: var(--base02) !important;
    --background-mod-strong: var(--base02) !important;
    --background-modifier-accent: var(--base02) !important;
    --background-modifier-active: var(--base02) !important;
    --background-modifier-hover: var(--base01) !important;
    --background-modifier-selected: var(--base01) !important;
    --background-primary: var(--base01) !important;
    --background-secondary-alt: var(--base01) !important;
    --background-secondary: var(--base00) !important;
    --background-surface-highest: var(--base02) !important;
    --background-surface-higher: var(--base02) !important;
    --background-surface-high: var(--base02) !important;
    --background-tertiary: var(--base00) !important;
    --background-base-low: var(--base01) !important;
    --background-base-lower: var(--base00) !important;
    --background-base-lowest: var(--base00) !important;
    --background-base-tertiary: var(--base00) !important;
    --background-code: var(--base02) !important;
    --background-mod-subtle: var(--base01) !important;
    --badge-notification-background: var(--base08) !important;
    --bg-base-secondary: var(--base00) !important;
    --bg-base-tertiary: var(--base00) !important;
    --bg-brand: var(--base03) !important;
    --bg-mod-faint: var(--base01) !important;
    --bg-overlay-2: var(--base01) !important;
    --bg-overlay-3: var(--base01) !important;
    --bg-overlay-color-inverse: var(--base03) !important;
    --bg-surface-raised: var(--base02) !important;
    --bg-surface-overlay: var(--base00) !important;
    --black: var(--base00) !important;
    --blurple-50: var(--base03) !important;
    --border-faint: var(--base02) !important;
    --border-subtle: var(--border-faint) !important;
    --brand-05a: var(--base01) !important;
    --brand-10a: var(--base01) !important;
    --brand-15a: var(--base01) !important;
    --brand-260: var(--base0D) !important;
    --brand-360: var(--base0D) !important;
    --brand-500: var(--base0D) !important;
    --brand-560: var(--base01) !important;
    --button-danger-background: var(--base08) !important;
    --button-danger-background-disabled: var(--base03) !important;
    --button-filled-brand-background: var(--base0D) !important;
    --button-filled-brand-background-hover: var(--base03) !important;
    --button-filled-brand-text: var(--base00) !important;
    --button-filled-brand-text-hover: var(--base05) !important;
    --button-outline-positive-border: var(--base0B) !important;
    --button-outline-danger-background-hover: var(--base08) !important;
    --button-outline-danger-border-hover: var(--base08) !important;
    --button-positive-background: var(--base0B) !important;
    --button-positive-background-disabled: var(--base03) !important;
    --button-positive-background-hover: var(--base03) !important;
    --button-secondary-background: var(--base02) !important;
    --button-secondary-background-disabled: var(--base03) !important;
    --button-secondary-background-hover: var(--base03) !important;
    --button-secondary-text: var(--color07) !important;
    --card-primary-bg: var(--base02) !important;
    --card-background-default: var(--base02) !important;
    --channel-icon: var(--base04) !important;
    --channels-default: var(--base03) !important;
    --channel-text-area-placeholder: var(--base03) !important;
    --channeltextarea-background: var(--base01) !important;
    --chat-background-default: var(--base01) !important;
    --chat-text-muted: var(--base03) !important;
    --checkbox-background-checked: var(--base0D) !important;
    --checkbox-border-checked: var(--base0D) !important;
    --checkbox-background-default: var(--base02) !important;
    --checkbox-border-default: var(--base03) !important;
    --control-brand-foreground-new: var(--base0D) !important;
    --control-brand-foreground: var(--base04) !important;
    --control-text-primary-default: var(--base00) !important;
    --control-background-primary-default: var(--color05) !important;
    --custom-notice-text: var(--base01) !important;
    --custom-poll-style-vote-percentage: var(--base04) !important;
    --deprecated-text-input-bg: var(--base01) !important;
    --deprecated-text-input-border: var(--base02) !important;
    --green-330: var(--base0B) !important;
    --green-360: var(--base0B) !important;
    --green-300: var(--base0B) !important;
    --header-primary: var(--base04) !important;
    --header-secondary: var(--base04) !important;
    --home-background: var(--base00) !important;
    --info-warning-foreground: var(--base0A) !important;
    --input-background: var(--base02) !important;
    --input-border: var(--base03) !important;
    --input-placeholder-text: var(--base03) !important;
    --interactive-active: var(--color07) !important;
    --interactive-hover: var(--color07) !important;
    --interactive-muted: var(--base03) !important;
    --interactive-normal: var(--color07) !important;
    --mention-background: var(--base03) !important;
    --mention-foreground: var(--color07) !important;
    --menu-item-danger-active-bg: var(--base08) !important;
    --menu-item-danger-hover-bg: var(--base08) !important;
    --menu-item-default-hover-bg: var(--base03) !important;
    --message-reacted-background: var(--base02) !important;
    --message-reacted-text: var(--base05) !important;
    --modal-background: var(--base01) !important;
    --modal-footer-background: var(--base00) !important;
    --notice-background-positive: var(--base0B) !important;
    --notice-text-positive: var(--base01) !important;
    --notice-background-warning: var(--base0A) !important;
    --notice-text-warning: var(--base01) !important;
    --notice-background-negative: var(--base08) !important;
    --notice-text-negative: var(--base01) !important;
    --opacity-blurple-24: var(--base02) !important;
    --plum-23: var(--base02) !important;
    --polls-victor-fill: var(--base0B) !important;
    --profile-gradient-button-color: var(--base02) !important;
    --primary-130: var(--base05) !important;
    --primary-300: var(--base05) !important;
    --primary-500: var(--base02) !important;
    --primary-600: var(--base00) !important;
    --primary-630: var(--base01) !important;
    --primary-660: var(--base00) !important;
    --primary-700: var(--base01) !important;
    --primary-800: var(--base00) !important;
    --red-400: var(--base08) !important;
    --red-460: var(--base08) !important;
    --red-500: var(--base08) !important;
    --red-630: var(--base08) !important;
    --red: var(--base08) !important;
    --red-new-22: var(--base08) !important;
    --red-new-46: var(--base08) !important;
    --redesign-input-control-selected: var(--base0B) !important;
    --scrollbar-auto-thumb: var(--base00) !important;
    --scrollbar-auto-track: transparent;
    --scrollbar-thin-thumb: var(--base00) !important;
    --scrollbar-thin-track: transparent;
    --search-popout-option-fade: none;
    --search-popout-option-non-text-color: var(--base07) !important;
    --status-danger-background: var(--base08) !important;
    --status-danger: var(--base08) !important;
    --status-negative: var(--base08) !important;
    --status-positive-background: var(--base0B) !important;
    --status-positive-text: var(--base0B) !important;
    --status-positive: var(--base0B) !important;
    --status-success: var(--base0B) !important;
    --status-warning-background: var(--base03) !important;
    --status-warning: var(--base09) !important;
    --teal-430: var(--base0C) !important;
    --text-brand: var(--color05) !important;
    --text-default: var(--color07) !important;
    --text-feedback-positive: var(--base0B) !important;
    --text-feedback-negative: var(--base08) !important;
    --text-feedback-warning: var(--base09) !important;
    --text-feedback-success: var(--base0B) !important;
    --text-link: var(--base0D) !important;
    --text-muted: var(--base03) !important;
    --text-negative: var(--base08) !important;
    --text-normal: var(--base0F) !important;
    --text-positive: var(--base0B) !important;
    --text-primary: var(--base0F) !important;
    --text-secondary: var(--base04) !important;
    --text-tertiary: var(--base03) !important;
    --text-warning: var(--base09) !important;
    --textbox-markdown-syntax: var(--base05) !important;
    --theme-base-color: var(--base00) !important;
    --user-profile-overlay-background: var(--base01) !important;
    --white-100: var(--base05) !important;
    --white-200: var(--base05) !important;
    --white-500: var(--base05) !important;
    --white: var(--color05) !important;
    --yellow-360: var(--base0A) !important;
    --yellow-300: var(--base0A) !important;
    --__lottieIconColor: var(--base03) !important;
    --redesign-button-secondary-background: var(--base03) !important;
}

/*--- Color Swaps ---*/
path[fill^="currentColor"],
svg[fill^="currentColor"],
rect[fill^="currentColor"] {
    fill: var(--color07) !important;
}

::selection {
    color: var(--base00);
    background: var(--base03);
}

.mention.interactive:hover {
    background-color: var(--base04) !important;
}

.default__459fb {
    background-color: var(--base07) !important;
}

.childWrapper__6e9f8 {
    background-color: var(--base02) !important;
}

svg[class^="closeIcon__"] path {
    fill: var(--base04) !important;
}

.invite__4d3fa {
    background: var(--base01) !important;
    border-color: var(--base02) !important;
}

.card__73069 {
    background-color: var(--base01);
}

div[class^="bar__"] {
    background-color: var(--base01) !important;
    border-color: var(--base02) !important;
}

.barText__7aaec {
    color: var(--base0B) !important;
}
.unreadIcon__7aaec {
    color: var(--base0B) !important;
}

.unreadPull__908e2 {
    color: var(--base02) !important;
}

.mentionsBar__7aaec .barText__7aaec {
    color: var(--base05) !important;
}

.container_f369db {
    background-color: var(--bg-overlay-2);
}

.circleIconButton__5bc7e {
    color: var(--base04);
}

.summariesBetaTag_cf58b5 {
    color: var(--base03);
}

div.folderIconWrapper__48112 {
    background-color: var(--base01) !important;
}

.numberBadge__2b1f5,
.textBadge__2b1f5 {
    color: var(--base02) !important;
}

.dots__5ad89 {
    color: var(--base02) !important;
}

.iconBadge__650eb {
    background-color: var(--base03);
}

.premiumIcon__5d473 {
    color: var(--base0F);
}

.progress__0d0f9 {
    background: var(--base0E) !important;
}

.callContainer_cb9592 {
    background-color: var(--base00);
}
.gradientContainer_bfe55a {
    background-image: var(--base00);
}

.gradient_e9ef78 {
    background: var(--base01) !important;
}
.bannerGradient__955a3 {
    background: var(--base00) !important;
}

.newMessagesBar__0f481 {
    background-color: var(--base03);

    button.barButtonAlt__0f481 {
        background-color: var(--base02) !important;
    }
}

.unreadPill__908e2 {
    color: var(--base01);
}

div[class*="numberBadge"] {
    color: var(--base05) !important;
}

.lookFilled__201d5.colorGreen__201d5,
.lookFilled__201d5.colorRed__201d5 {
    color: var(--base00) !important;
}

.folderGroupBackground__48112 {
    border: none;
}

* {
    text-rendering: optimizeLegibility !important;
}

/*--- Codeblock syntax highlighting ---*/
.hljs-ansi-foreground-red {
    color: var(--base08) !important;
}
.hljs-ansi-foreground-green {
    color: var(--base0B) !important;
}
.hljs-ansi-foreground-yellow {
    color: var(--base0A) !important;
}
.hljs-ansi-foreground-blue {
    color: var(--base0D) !important;
}
.hljs-ansi-foreground-magenta {
    color: var(--base0E) !important;
}
.hljs-attr {
    color: var(--base06) !important;
}
.hljs-attribute {
    color: var(--base06) !important;
}
.hljs-number {
    color: var(--base06) !important;
}
.hljs-selector-class {
    color: var(--base06) !important;
}
.hljs-comment {
    color: var(--base03) !important;
}
.hljs-subst {
    color: var(--base0D) !important;
}
.hljs-selector-pseudo {
    color: var(--base0B) !important;
}
.hljs-section {
    color: var(--base0B) !important;
}
.hljs-keyword {
    color: var(--base08) !important;
}
.hljs-variable {
    color: var(--base08) !important;
}
.hljs-meta {
    color: var(--base03) !important;
}
.hljs-built_in {
    color: var(--base09) !important;
}
.hljs-string {
    color: var(--base0B) !important;
}
.hljs-title {
    color: var(--base0E) !important;
}

/*--- Visual refresh recolor ---*/
.visual-refresh {
    div[class^="autocomplete__"] {
        background-color: var(--base02) !important;
    }
    path[fill^="rgba(88, 101, 242, 1)"] {
        fill: var(--base0B) !important;
    }
    div[class^="topicsPillContainer"] {
        --bg-overlay-2: var(--base02) !important;
    }
    .tagPill__9a337 {
        background-color: var(--base00) !important;
    }
    .bg__960e4 {
        background: var(--base00) !important;
    }
    .wrapper_ef3116 {
        background-color: var(--base00) !important;
    }
    .sidebar_c48ade {
        background-color: var(--base00) !important;
    }
    .searchBar__97492 {
        background-color: var(--base02) !important;
    }
    .channelTextArea_f75fb0 {
        background: var(--base01) !important;
    }
    .chatContent_f75fb0 {
        background-color: var(--base00) !important;
    }
    .members_c8ffbb,
    .member_c8ffbb {
        background: var(--base00) !important;
    }
    .voiceBar__7aaec {
        background-color: var(--base02) !important;
    }
    button.button__67645.redGlow__67645,
    span.button__67645.redGlow__67645 {
        background-color: var(--base02) !important;
    }
    .experimentButton_e131a9.buttonColor_e131a9.buttonActive_e131a9 {
        background-color: var(--base0B) !important;
        color: var(--base00) !important;
    }
    .selectedBackground_e681d1 {
        background-color: var(--base02) !important;
    }
    svg[fill^="#d83a42"],
    rect[fill^="#d83a42"],
    path[fill^="#d83a42"],
    svg[fill^="#d83a41"],
    rect[fill^="#d83a41"],
    path[fill^="#d83a41"] {
        fill: var(--status-danger) !important;
    }
    svg[fill^="#ca9654"],
    rect[fill^="#ca9654"],
    path[fill^="#ca9654"],
    svg[fill^="#cc954c"],
    rect[fill^="#cc954c"],
    path[fill^="#cc954c"] {
        fill: var(--status-warning) !important;
    }
    path[fill^="#43a25a"],
    svg[fill^="#43a25a"],
    rect[fill^="#43a25a"],
    path[fill^="#40a258"],
    svg[fill^="#40a258"],
    rect[fill^="#40a258"] {
        fill: var(--status-positive) !important;
    }
    svg[fill^="#83838b"],
    rect[fill^="#83838b"],
    path[fill^="#83838b"],
    svg[fill^="#82838b"],
    rect[fill^="#82838b"],
    path[fill^="#82838b"] {
        fill: var(--base03) !important;
    }
}

.theme-light {
    --base01: color-mix(in srgb, var(--color00) 95%, black) !important;
    --base02: color-mix(in srgb, var(--color00) 85%, black) !important;
    --base03: color-mix(in srgb, var(--color00) 80%, black) !important;
    --base04: color-mix(in srgb, var(--color00) 70%, black) !important;
    --base06: color-mix(in srgb, var(--color05) 95%, white) !important;
    --base07: color-mix(in srgb, var(--color05) 90%, white) !important;
}