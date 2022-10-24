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
| repository    | <b><a href="{{repository}}" target="_blank">Source code</a></b> |
| tags       | {% if tags != "" %}{{ tags }}{% endif %} |

## Description  
{{ description }}

## Lineage 
This workspace has features of the following workspaces (build history)
{{ lineage_table }}

## UI tabs and ports
UI shortcuts for apps and their respective ports (allowed port range is 8021-8040)
{{ ports_table }}

## Apps & services
Commads used to start apps and services in the workspace
{{ startup_table }}
"""


supervisord_template = """
[program:{{ name }}]
command=/bin/sh -c "{% if env_vars is defined %}{% for env in env_vars %}export {{env}}; {% endfor %}{% endif %}{% if folder is defined %}cd {{folder}}; {% endif %} {{ cmd }}"
stderr_logfile = /var/log/workspace/{{ name }}-stderr.log
stdout_logfile = /var/log/workspace/{{ name }}-stdout.log
logfile_maxbytes = 1024
"""

port_usage_template = """
| Port      | Application                          | Tab      |
| ----------- | ------------------------------------ | ----------- |
{% for p in data.ports -%}
| {{p.port}}       | {{p.title}}        | {{p.page}}      |
{% endfor %}
"""

startup_apps_template = """
| Application      | Command                          |
| ----------- | ------------------------------------ |
{% for p in data.startup_apps -%}
| {{p.app}}       | {{p.cmd}}        |
{% endfor %}
"""

lineage_template = """
| Layer      | Name                          | Version      | Tags      |
| ----------- | --------------------------- | ----------- | ----------- |
{% for l in data.lineage -%}
| {{l.ind}}       | [{{l.name}}]({{l.link}})        | {{l.version}}      |  {% if l.tags != "" %}{{ l.tags }}{% endif %}     |
{% endfor %}
"""

cheatsheet_template = """

{% for section, commands in data.items() -%}
## {{section}}
{% for code, cmdict in commands.items() -%}
- `{{cmdict.cmd}}` - {{cmdict.description}}
{% endfor %}
{% endfor %}

<style>
/* Add TOC to this page */
.md-sidebar.md-sidebar--secondary {
    display: block !important;
}
</style>
"""

links_template = """

{% for section, links in data.items() -%}
## {{section}}
{% for code, link in links.items() -%}
- <b><a href="{{link.url}}" target="_blank">{{link.name}}</a></b> - {{link.description}}
{% endfor %}
{% endfor %}

<style>
/* Add TOC to this page */
.md-sidebar.md-sidebar--secondary {
    display: block !important;
}
</style>
"""

frpc_http_template = """
[common]
server_addr = {{data.server_url}}
server_port = {{data.server_port}}              
token = {{data.token}}    
tcp_mux = true
tls_enable = true

[web]
type = http
local_port = {{data.local_port}}                           
subdomain = {{data.subdomain}}         
use_encryption = true
use_compression = true
bandwidth_limit = {{data.bandwidth_limit}}
"""