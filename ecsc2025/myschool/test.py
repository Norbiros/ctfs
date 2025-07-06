from jinja2 import Template
absd = 1
print(Template("""
{% for c in ''.__class__.__mro__[1].__subclasses__() %}
    {{ loop.index }}: {{ c }}
{% endfor %}

""").render())
