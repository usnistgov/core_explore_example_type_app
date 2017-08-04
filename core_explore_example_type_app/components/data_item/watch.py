"""
Handle signals.
"""
from signals_utils.signals.mongo import connector, signals
from core_main_app.components.data.models import Data
from core_explore_example_type_app.components.data_item import api as data_item_api


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
        data_item_api.generate_data_items_from_data(document)
    except Exception as e:
        pass
        # TODO: If something went wrong, do we delete the data and raise an exception?
        # delete(data)
        # raise exceptions.ApiError("Unable to save data")
