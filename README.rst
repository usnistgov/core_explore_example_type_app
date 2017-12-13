core_explore_example_type_app
=============================

Exploration by example type for the curator core project.

Quick start
===========

1. Add "core_explore_example_type_app" to your INSTALLED_APPS setting
---------------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_explore_example_type_app',
    ]

2. Include the core_explore_example_type_app URLconf in your project urls.py
----------------------------------------------------------------------------

.. code:: python

    url(r'^explore/type/example/', include('core_explore_example_type_app.urls')),
