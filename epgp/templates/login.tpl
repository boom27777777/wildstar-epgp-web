{% extends 'base.tpl' %}
{% block content -%}
    <div class="col-lg-2 col-lg-offset-3 col-xs-12 well">
        <form action="/login" method="post">
            <input type="text" class="form-control" placeholder="Username" name="username"/>
            <input type="password" class="form-control" placeholder="Password" name="password"/>
            <button class="btn-block">Login</button>
        </form>
    </div>
{% endblock -%}
