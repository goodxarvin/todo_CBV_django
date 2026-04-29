{% extends "mail_templated/base.tpl" %}


{% block subject %}
Hello {{ name }} 
{% endblock %}

{% block body %}
This is a plain text part.
{% endblock %}

{% block html %}
your verification url:
<a href="{{ access_token }}">{{ access_token }}</a>

<!-- put in both places to show the url -->

<!-- <img src="https://gapgpt.app/model_icons/gapgpt-purple-icon-v3.png" alt=""> -->


{% endblock %}