styles_str = """
[data-md-color-scheme="workspace"] {
    --md-primary-fg-color:          {{ styles.light.primary|default('#2A2D2E') }};
    --md-accent-fg-color:           {{ styles.light.accent|default('#E77260') }};
    --md-default-bg-color:          {{ styles.light.background|default('#E9EAE6') }};
    --md-default-fg-color--light:   {{ styles.light.subtitle|default('#E77260') }};
    --md-typeset-color:             {{ styles.light.text|default('#1C1C1C') }};
    --md-typeset-a-color:           {{ styles.light.title|default('#1C1C1C') }};
    --md-code-bg-color:             {{ styles.light.code_background|default('#D2D2D2') }};
    --md-code-fg-color:             {{ styles.light.code_text|default('#D2D2D2') }};
}
[data-md-color-scheme="workspace-dark"] {
    --md-primary-fg-color:          {{ styles.dark.primary|default('#3C3C3C') }};
    --md-accent-fg-color:           {{ styles.dark.accent|default('#E77260') }};
    --md-default-bg-color:          {{ styles.dark.background|default('#1E1E1E') }};
    --md-default-fg-color--light:   {{ styles.dark.subtitle|default('#9CDCFE') }};
    --md-typeset-color:             {{ styles.dark.text|default('#9CDCFE') }};
    --md-typeset-a-color:           {{ styles.dark.title|default('#9CDCFE') }};
    --md-code-bg-color:             {{ styles.dark.code_background|default('#D2D2D2') }};
    --md-code-fg-color:             {{ styles.dark.code_text|default('#bfbfbf') }};
}

{% if 'common_colors' in styles %}
{% if 'header' in styles['common_colors'] %}
.md-header {
    color: {{ styles.common_colors.header }}; !important;
    }
{% endif %}
{% endif %}

.md-nav__link--active {
    color: {{ styles.common_colors.nav|default('#eab676') }} !important;
}
"""