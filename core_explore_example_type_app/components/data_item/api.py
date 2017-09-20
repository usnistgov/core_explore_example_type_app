""" Data Item API
"""

from core_explore_example_type_app.components.data_item.access_control import \
    get_user_readable_data
from core_explore_example_type_app.components.data_item.models import DataItem
from core_main_app.utils.access_control.decorators import access_control


def get_by_data(data):
    """ Return a Data Item with the data given.

    Args:
        data:

    Returns:

    """
    return DataItem.get_by_data(data)


def upsert(data_item):
    """ Upsert data item.

    Args:
        data_item:

    Returns:

    """
    return data_item.save()


def delete_from_data_if_exists(data):
    """ Delete data item relative to the given data

    Args:
        data:

    Returns:

    """
    try:
        DataItem.delete_from_data(data)
    except Exception:
        pass


@access_control(get_user_readable_data)
def execute_query_distinct_by_data(query, user):
    """Execute a query on the DataItem collection distinct by data.

    Args:
        query:

    Returns:

    """
    return DataItem.execute_query_distinct_by_data(query)
