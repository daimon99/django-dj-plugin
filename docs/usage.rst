=====
Usage
=====

To use django-dj-plugin in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_dj_plugin.apps.DjangoDjPluginConfig',
        ...
    )

Add django-dj-plugin's URL patterns:

.. code-block:: python

    from django_dj_plugin import urls as django_dj_plugin_urls


    urlpatterns = [
        ...
        url(r'^', include(django_dj_plugin_urls)),
        ...
    ]
