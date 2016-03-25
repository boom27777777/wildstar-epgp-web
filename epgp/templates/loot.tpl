{% extends 'base.tpl' %}
{% block content -%}
    <div class="content col-lg-6 col-lg-offset-1">
        {% if guild.logs -%}
            <table class="table table-responsive">
                <thead>
                <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Who</th>
                    <th>Item</th>
                    <th class="text-right">Amount</th>
                    <th class="text-right">Total</th>
                </tr>
                </thead>
                <tbody>
                {% set day = '' %}
                {% for raider, entry in guild.logs -%}
                    {% if day != entry.strDate %}
                        <tr class="break"></tr>
                    {% endif %}
                    {% set day = entry.strDate %}
                    <tr>
                        <td>{{ entry.strDate }}</td>
                        <td>{{ entry.strTime }}</td>
                        <td>{{ raider }}</td>
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
