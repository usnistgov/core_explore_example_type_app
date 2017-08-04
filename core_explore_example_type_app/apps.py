""" Apps file for setting example type when app is ready
"""
from django.apps import AppConfig

import core_explore_example_type_app.components.data_item.discover as discover_data
from core_explore_example_type_app.components.data_item import watch as data_watch


class ExampleTypeAppConfig(AppConfig):
    """ Core application settings
    """
    name = 'core_explore_example_type_app'

    def ready(self):
        """ Run when the app is ready

        Returns:

        """
        # TODO: Could be done in Celery
        discover_data.generate_data_item_from_data()

        data_watch.init()
