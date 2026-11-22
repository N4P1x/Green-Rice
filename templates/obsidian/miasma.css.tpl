/* Miasma Obsidian theme.
 * Install: copy to YourVault/.obsidian/snippets/miasma.css, enable in
 * Settings -> Appearance -> CSS snippets.
 */

.theme-dark, .theme-light {
  /* Core colors */
  --background-primary: #{{bg}};
  --background-primary-alt: #{{bg}};
  --background-secondary: #{{bg}};
  --background-secondary-alt: #{{bg}};
  --text-normal: #{{fg}};

  /* Selection colors */
  --text-selection: #{{selection}};

  /* Border color */
  --background-modifier-border: #{{fg_muted}};

  /* Semantic heading colors */
  --text-title-h1: #{{red}};
  --text-title-h2: #{{green}};
  --text-title-h3: #{{yellow}};
  --text-title-h4: #{{accent}};
  --text-title-h5: #{{magenta}};
  --text-title-h6: #{{magenta}};

  /* Links and accents */
  --text-link: #{{accent}};
  --text-accent: #{{accent}};
  --text-accent-hover: #{{accent}};
  --interactive-accent: #{{accent}};
  --interactive-accent-hover: #{{accent}};

  /* Muted text */
  --text-muted: color-mix(in srgb, #{{fg}} 70%, transparent);
  --text-faint: color-mix(in srgb, #{{fg}} 55%, transparent);

  /* Code */
  --code-normal: #{{cyan}};

  /* Errors and success */
  --text-error: #{{red}};
  --text-error-hover: #{{red}};
  --text-success: #{{green}};

  /* Tags */
  --tag-color: #{{cyan}};
  --tag-background: #{{fg_muted}};

  /* Graph */
  --graph-line: #{{fg_muted}};
  --graph-node: #{{accent}};
  --graph-node-focused: #{{accent}};
  --graph-node-tag: #{{cyan}};
  --graph-node-attachment: #{{green}};
}

/* Headers */
.cm-header-1, .markdown-rendered h1 { color: var(--text-title-h1); }
.cm-header-2, .markdown-rendered h2 { color: var(--text-title-h2); }
.cm-header-3, .markdown-rendered h3 { color: var(--text-title-h3); }
.cm-header-4, .markdown-rendered h4 { color: var(--text-title-h4); }
.cm-header-5, .markdown-rendered h5 { color: var(--text-title-h5); }
.cm-header-6, .markdown-rendered h6 { color: var(--text-title-h6); }

/* Code blocks */
.markdown-rendered code {
  color: #{{cyan}};
}

/* Syntax highlighting */
.cm-s-obsidian span.cm-keyword { color: #{{red}}; }
.cm-s-obsidian span.cm-string { color: #{{green}}; }
.cm-s-obsidian span.cm-number { color: #{{yellow}}; }
.cm-s-obsidian span.cm-comment { color: #{{fg_muted}}; }
.cm-s-obsidian span.cm-operator { color: #{{accent}}; }
.cm-s-obsidian span.cm-def { color: #{{accent}}; }

/* Links */
.markdown-rendered a {
  color: var(--text-link);
}

/* Blockquotes */
.markdown-rendered blockquote {
  border-left-color: #{{accent}};
}

/* Active elements */
.workspace-leaf.mod-active .workspace-leaf-header-title {
  color: var(--interactive-accent);
}

.nav-file-title.is-active {
  color: var(--interactive-accent);
}

/* Search results */
.search-result-file-title {
  color: var(--interactive-accent);
}