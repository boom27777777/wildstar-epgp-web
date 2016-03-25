{% extends "base.tpl" -%}
{% block sidebar -%}
    <div class="col-lg-3">
        <div class="raider-name well text-center">
            <h1 class="raider-name">
                {{ raider.name }}
                {% if raider.alts -%}
                {% endif -%}
                {% for alt in raider.alts -%}
                    <div>
                        <small>{{ alt.name }}</small>
                    </div>
                {% endfor -%}
            </h1>
            <hr class="class-sep"/>
            <h2>
                <small>{{ raider.role }}|{{ raider.class_name }}</small>
            </h2>
            <h3 class="well">
                PR: {{ "%0.3f" | format(raider.pr) }} <br/>
                <small>EP: {{ raider.ep }} | GP: {{ raider.gp }}</small>
            </h3>
            <ul class="raider-nav nav nav-pills nav-stacked text-center">
                <li class="list-group-item"><a href="/">Back</a></li>
            </ul>
        </div>
    </div>
{% endblock -%}
{% block content -%}
    {% if raider.armory -%}
        <div id="armory" class="col-lg-3 col-xs-12 well">
            {% for item in raider.gear %}
                <div class="gear-slot well col-lg-4 col-xs-4 text-center">
                    <a href="http://www.jabbithole.com/items/i-{{ item.id }}"><img src="" alt=""/></a>
                </div>
            {% endfor %}

        </div>
    {% endif -%}
    <div class="raider-logs col-lg-6 col-xs-12">
        {% if raider.logs -%}
            <table class="table table-responsive table-bordered">
                <thead>
                <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Type</th>
                    <th>Comment</th>
                    <th class="text-right">Amount</th>
                    <th class="text-right">Total</th>
                </tr>
                </thead>
                <tbody>
                {% for entry in raider.logs -%}
                    {% if entry.Type == 'EP' %}
                        <tr class="ep-row">
                            {% elif entry.Type == 'GP' %}
                        <tr class="gp-row">
                            {% elif entry.Type == 'Decay' %}
                        <tr class="decay-row">
                            {% else %}
                        <tr>
                    {% endif %}
                <td>{{ entry.strDate }}</td>
                <td>{{ entry.strTime }}</td>
                <td>{{ entry.Type }}</td>
                <td>{{ entry.strComment }}</td>
                <td class="text-right">{{ entry.strModifier }}</td>
                <td class="text-right">{{ entry.nAfter }}</td>
                </tr>
                {% endfor -%}
                </tbody>
            </table>
        {% endif -%}
    </div>
{% endblock -%}
