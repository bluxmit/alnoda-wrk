
styles_str = """
{% if 'light' in styles %} 
[data-md-color-scheme="workspace"] {
{% if 'primary' in styles['light'] %} 
    --md-primary-fg-color:        {{ styles.light.primary }};
{% endif %}
{% if 'accent' in styles['light'] %} 
    --md-accent-fg-color:        {{ styles.light.accent }};
{% endif %}

{% if 'background' in styles['light'] %} 
    --md-default-bg-color:        {{ styles.light.background }};
{% endif %}
{% if 'subtitle' in styles['light'] %} 
    --md-default-fg-color--light:        {{ styles.light.subtitle }};
{% endif %}
{% if 'text' in styles['light'] %} 
    --md-typeset-color:        {{ styles.light.text }};
{% endif %}
{% if 'title' in styles['light'] %} 
    --md-typeset-a-color:        {{ styles.light.title }};
{% endif %}
}
{% endif %}

{% if 'dark' in styles %} 
[data-md-color-scheme="workspace-dark"] {
{% if 'primary' in styles['dark'] %} 
    --md-primary-fg-color:        {{ styles.dark.primary }};
{% endif %}
{% if 'accent' in styles['dark'] %} 
    --md-accent-fg-color:        {{ styles.dark.accent }};
{% endif %}

{% if 'background' in styles['dark'] %} 
    --md-default-bg-color:        {{ styles.dark.background }};
{% endif %}
{% if 'subtitle' in styles['dark'] %} 
    --md-default-fg-color--light:        {{ styles.dark.subtitle }};
{% endif %}
{% if 'text' in styles['dark'] %} 
    --md-typeset-color:        {{ styles.dark.text }};
{% endif %}
{% if 'title' in styles['dark'] %} 
    --md-typeset-a-color:        {{ styles.dark.title }};
{% endif %}
}
{% endif %}


{% if 'common_colors' in styles %}
{% if 'header' in styles['common_colors'] %}
.md-header {
    color: {{ styles.common_colors.header }}; !important;
    }
{% endif %}
{% if 'nav' in styles['common_colors'] %}
.md-nav__link--active {
    color: {{ styles.common_colors.nav }} !important;
}
{% endif %}
{% endif %}
"""
