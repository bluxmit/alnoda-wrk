app_page_str = """
<div class="quickstart-wrapper">
  {% set page_apps = get_page_apps('PAGE_NAME_REPLACE') %}
  {% for tool in page_apps %}
    <div>
        <a href="{{ tool.app_url }}" target="_blank" rel="noopener noreferrer">
            <img src="{{ tool.image }}" class="tool-img"/>
        </a>
        <a href="{{ tool.app_url }}">
            <div class="tool-caption">{{ tool.title }}</div>
        </a>
        <div class="tool-description">{{ tool.description }}</div>
    </div>
  {% endfor %}
</div>
"""


about_page_template = """
## About

| Name      | {{ name }}                          |
| ----------- | ------------------------------------ |
| version       | {{ version }} |
| author       | {{ author }} |
| created    | {{ created }} |

## Description  

{{ description }}
"""


supervisord_template = """
[program:{{ name }}]
command=/bin/sh -c "{% if env_vars is defined %}{% for env in env_vars %}export {{env}}; {% endfor %}{% endif %}{% if folder is defined %}cd {{folder}}; {% endif %} {{ cmd }} "
stderr_logfile = /var/log/workspace/{{ name }}-stderr.log
stdout_logfile = /var/log/workspace/{{ name }}-stdout.log
logfile_maxbytes = 1024
"""