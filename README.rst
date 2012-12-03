==============
django-jasmine
==============

django-jasmine integrates the
`Jasmine Javascript testing framework <http://pivotal.github.com/jasmine/>`_
with `Django <http://www.djangoproject.com/>`_.  Jasmine is a behavior-driven
development framework for testing your JavaScript code. It does not depend on
any other JavaScript frameworks.  It does not require a DOM. And it has a
clean, obvious syntax so that you can easily write tests.

django-jasmine version 1.0 includes jasmine v1.3.0.


Installation
============

1. ``pip install django-jasmine``

2. Add ``django_jasmine`` to your project settings::

    INSTALLED_APPS = (
        # ...
        'django_jasmine',
    )

3. Add the jasmine test runner to the end of your base urlconf::

    from django.conf import settings
    from django_jasmine.views import RunTests

    patterns = urlpatterns('',
        # Current urls
    )

    if settings.DEBUG:
        patterns += urlpatterns('',
            url('^js_tests/$', RunTests.as_view(), name='jasmine_tests'),
        )


Usage
=====

django-jasmine looks throughout your static files locations for ``tests.json``
configuration files.

These files should contain references to spec files (the tests), other
javascript (libraries and supporting files), and templates to include
(such as javascript templates). For example::

    {
        "spec": [
            "js/myapp/tests.js"
        ],
        "js": [
            "//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js",
            "js/lib/underscore.js",
            "js/lib/backbone.js",
            "js/base.js",
            "js/myapp/models.js",
            "js/myapp/views.js"
        ],
        "templates": [
            "myapp/javascript/myapp.html"
        ]
    }

If you want to use separate configuration files for each of your project's
apps, you can put the common scripts in a project-level config. To ensure these
common scripts are ordered first, set the ``priority`` key in your config file
to ``true``. For example::

    {
        "priority": true,
        "js": [
            "//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js",
            "js/lib/underscore.js",
            "js/lib/backbone.js",
            "js/base.js"
        ]
    }


Test Template
=============

If you wish to modify the jasmine index template for any reason (e.g. add a new
jasmine reporter), you can create a jasmine/index.html template as follow::

    {% extends "jasmine/base.html" %}

    {% block extrajs %}
        {# If you want to extend the default jasmine config or add other media #}
    {% endblock %}

    {% block jasmine %}
        {# If you wish to rewrite the whole html runner script #}
    {% endblock %}


See ``django_jasmine/templates/jasmine/base.html`` for the default config.
