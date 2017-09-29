"""Util to build queries for mongo db
"""

from core_explore_example_app.utils import mongo_query as common_mongo_query
from core_explore_example_type_app.components.data_structure_type_element import api as \
    data_structure_type_element_api
from core_main_app.commons import exceptions


def fields_to_query(form_values, template_id):
    """Takes values from the html tree and creates a query from them

    Args:
        form_values:
        template_id:

    Returns:

    """
    # FIXME: Refactor mongo_query to avoid passing a function in parameter.
    return common_mongo_query.fields_to_query_custom_dot_notation(form_values, template_id,
                                                                  get_dot_notation_to_element,
                                                                  use_wildcard=True)


def get_dot_notation_to_element(data_structure_element, namespaces):
    """Get the dot notation of the data_structure_element.

    Args:
        data_structure_element:
        namespaces:

    Returns:

    """
    # get data structure element's xml xpath.
    try:
        data_structure_type_element = data_structure_type_element_api.get_by_data_structure_id(
            str(data_structure_element.id))
        # get dot_notation
        path = data_structure_type_element.path
        # replace '/' by '.' (Avoid first '/')
        dot_notation = path[1:].replace("/", ".")
    except (exceptions.DoesNotExist, exceptions.ModelError, Exception):
        dot_notation = ""

    return dot_notation
