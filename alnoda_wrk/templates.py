app_page_str = """
<div class="quickstart-wrapper">
  {% set page_apps = get_page_apps('my_apps') %}
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
{% if folder is defined %}directory={{folder}}{% endif %}
command=/bin/sh -c " {{ cmd }} "
stderr_logfile = /var/log/workspace/{{ name }}-stderr.log
stdout_logfile = /var/log/workspace/{{ name }}-stdout.log
logfile_maxbytes = 1024
"""