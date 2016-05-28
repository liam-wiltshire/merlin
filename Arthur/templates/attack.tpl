{% from 'macros.tpl' import planetlink, galaxyscanslink, alliancelink with context %}
{% extends "base.tpl" %}
{% set cols = 9 + waves|count %}
{% if user|intel %}{% set cols = cols + 1 %}{% endif %}
{% block content %}
{% if message %}
    <p>{{ message }}</p>
{% endif %}
    <table cellpadding="3" cellspacing="1" width="95%" class="black">
        <tr class="datahigh"><th colspan="{{cols}}">
            Attack {{ attack.id }} LT: {{ attack.landtick }} {{ attack.comment }}
        </th></tr>
        <tr class="header">
            <th>Coords</th>
            <th>Race</th>
            <th>Size</th>
            <th>Value</th>
            <th>Score</th>
            <th>Scans</th>
            <th>Amps / Dists / Tech</th>
            {%- for lt in waves %}
            <th>ETA {{lt-tick}} ({{lt}})</th>
            {% endfor -%}
            <th><a href="" onclick="toggleGrowth();return false;">Size</a></th>
            <th><a href="" onclick="toggleGrowth();return false;">Value</a></th>
            {% if user|intel %}
            <th>Intel</th>
            {% endif %}
        </tr>
        
        {% for planet, scans, bookings in group %}
        <tr class="{{ loop.cycle('odd', 'even') }}">
            <td class="center"><a {{galaxyscanslink(planet.galaxy)}}>{{ planet.x }}:{{ planet.y }}</a> <a {{planetlink(planet)}}>{{ planet.z }}</a></td>
            <td class="center {{ planet.race }}">{{ planet.race }}</td>
            <td class="right"> {{ planet.size|intcomma }} </td>
            <td class="right"> {{ planet.value|intcomma }} </td>
            <td class="right"> {{ planet.score|intcomma }} </td>
            <td class="center">
                {% for scan in scans %}
                    {% set scanage = update.id - scan.tick %}
                    <a href="attack/{{ attack.id }}/#{{ scan.pa_id }}" onclick="return linkshift(event, '{{ scan.link|url }}');" class="scan_age_{% 
                        if scanage > 12 %}ancient{% elif scanage > 5 %}older{% elif scanage > 0 %}old{% else %}new{% endif %}">{{ scan.scantype }}</a>
                {% endfor %}
            </td>
            {% if planet.intel %}
                {% set scan = planet.scan("D") %}
                {% with dscan = scan.devscan %}
                <td class="center">{{planet.intel.amps}} / {{ planet.intel.dists}} / {{dscan.waves_str()[:1] if dscan else "?"}}</td>
                {% endwith %}
            {% else %}
                <td class="center">? / ? / ?</td>
            {% endif %}
                {% for lt, target in bookings %}
            <td class="center">
                    {%- if target and target.user == user %}
                        <b><i>
                        <a href="{% url "unbook", attack.id, planet.x, planet.y, planet.z, lt %}">{{ target.user.name }}</a>
                        </i></b>
                    {%- elif target %}
                        <b><i>
                        {{ target.user.name }}
                        </i></b>
                    {%- elif target == false %}
                        unclaimed
                    {%- elif target is none %}
                        <a href="{% url "book", attack.id, planet.x, planet.y, planet.z, lt %}">book</a>
                    {%- endif -%}
            </td>
                {% endfor %}
            <td align="right">{{ planet|growth("size") }}</td>
            <td align="right">{{ planet|growth("value") }}</td>
            {% if user|intel %}
                {% if planet.intel %}
                <td class="center">{%if planet.alliance %}A:<a {{alliancelink(planet.alliance.name)}}>{{ planet.alliance.name }}</a>{% endif %}{%if planet.intel.nick %} N:{{ planet.intel.nick }}{% endif %}</td>
                {% else %}
                <td class="center"></td>
                {% endif %}
            {% endif %}
        </tr>
        {% endfor %}
    </table>
    
    {% for scan in scans %}
    <p>&nbsp;</p>
    {% include "scans/scan.tpl" %}
    {% endfor %}
{% endblock %}
