# core_explore_example_type_app

core_explore_example_type_app is a Django app.

# Quick start

1. Add "core_explore_example_type_app" to your INSTALLED_APPS setting like this:

  ```python
  INSTALLED_APPS = [
      ...
      'core_explore_example_type_app',
  ]
  ```

  2. Include the core_explore_example_type_app URLconf in your project urls.py like this::

  ```python
  url(r'^explore/type/example', include('core_explore_example_type_app.urls')),
  ```

