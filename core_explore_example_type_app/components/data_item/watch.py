"""
Handle signals.
"""
from signals_utils.signals.mongo import connector, signals

import core_explore_example_type_app.tasks as explore_example_type_task
from core_main_app.components.data.models import Data


def init():
    """ Connect to Data object events.
    """
    connector.connect(post_save_data, signals.post_save, Data)


def post_save_data(sender, document, **kwargs):
    """ Method executed after a saving of a Data object.
    Args:
        sender: Class.
        document: Data document.
        **kwargs: Args.

    """
    try:
        # generate all item from the data
        explore_example_type_task.generate_data_items_from_data.delay(str(document.id))
    except Exception as e:
        pass
        # TODO: If something went wrong, do we delete the data and raise an exception?
        # delete(data)
        # raise exceptions.ApiError("Unable to save data")
