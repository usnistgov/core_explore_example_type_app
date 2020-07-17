""" Apps file for setting example type when app is ready
"""
from django.apps import AppConfig


class ExampleTypeAppConfig(AppConfig):
    """ Core application settings
    """

    name = "core_explore_example_type_app"

    def ready(self):
        """ Run when the app is ready

        Returns:

        """
        # import have to be made when apps are ready, not before,
        # so not at the beginning of the file
        import core_explore_example_type_app.tasks as explore_example_type_tasks
        from core_explore_example_type_app.components.data_item import (
            watch as data_watch,
        )

        # start asynchronous task
        explore_example_type_tasks.generate_data_items_from_all_data_in_database.delay()
        data_watch.init()
