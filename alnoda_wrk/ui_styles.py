styles_str = """
[data-md-color-scheme="workspace"] {
    --md-primary-fg-color:          {{ styles.light.primary|default('#2A2D2E') }};
    --md-accent-fg-color:           {{ styles.light.accent|default('#E77260') }};
    --md-default-bg-color:          {{ styles.light.background|default('#E9EAE6') }};
    --md-typeset-color:             {{ styles.light.text|default('#1C1C1C') }};
    --md-typeset-a-color:           {{ styles.light.title|default('#1C1C1C') }};
    --md-code-bg-color:             {{ styles.light.code_background|default('#D2D2D2') }};
    --md-code-fg-color:             {{ styles.light.code_text|default('#4d4c4c') }};
}
[data-md-color-scheme="workspace-dark"] {
    --md-primary-fg-color:          {{ styles.dark.primary|default('#3C3C3C') }};
    --md-accent-fg-color:           {{ styles.dark.accent|default('#E77260') }};
    --md-default-bg-color:          {{ styles.dark.background|default('#1E1E1E') }};
    --md-typeset-color:             {{ styles.dark.text|default('#9CDCFE') }};
    --md-typeset-a-color:           {{ styles.dark.title|default('#9CDCFE') }};
    --md-code-bg-color:             {{ styles.dark.code_background|default('#2e2b2b') }};
    --md-code-fg-color:             {{ styles.dark.code_text|default('#ced6d6') }};
}

.md-header {
    color: {{ styles.common_colors.header|default('#FFFFFF') }}; !important;
    }

.md-nav__link--active {
    color: {{ styles.common_colors.nav|default('#eab676') }} !important;
}
"""