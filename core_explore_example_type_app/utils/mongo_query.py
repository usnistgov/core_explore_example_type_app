"""Util to build queries for mongo db
"""
import json
from xml_utils.xsd_types.xsd_types import get_xsd_numbers, get_xsd_floating_numbers
from core_explore_example_app.utils import mongo_query as common_mongo_query


def build_enum_criteria(path, value, is_not=False):
    """Builds a criteria for an enumeration

    Args:
        path:
        value:
        is_not:

    Returns:

    """
    criteria = dict()

    if is_not:
        criteria[path] = json.loads('{{"ne": "{0}" }}'.format(repr(value)))
    else:
        criteria[path] = value

    key, value = criteria.popitem()
    criteria_key = {'path': "/.*{}/".format(key)}
    criteria_value = {'value': value}
    criteria = common_mongo_query.build_and_criteria(criteria_key, criteria_value)

    return criteria


def build_criteria(element_path, comparison, value, element_type, default_prefix, is_not=False):
    """Looks at element type and route to the right function to build the criteria

    Args:
        element_path:
        comparison:
        value:
        element_type:
        default_prefix:
        is_not:

    Returns:

    """
    # build the query: value can be found at element:value or at element.#text:value
    # second case appends when the element has attributes or namespace information
    if element_type in get_xsd_numbers(default_prefix):
        element_query = common_mongo_query.build_int_criteria(element_path, comparison, value)
        attribute_query = common_mongo_query.build_int_criteria("{}.#text".format(element_path),
                                                                comparison, value)
    elif element_type in get_xsd_floating_numbers(default_prefix):
        element_query = common_mongo_query.build_float_criteria(element_path, comparison, value)
        attribute_query = common_mongo_query.build_float_criteria("{}.#text".format(
            element_path), comparison, value)
    else:
        element_query = common_mongo_query.build_string_criteria(element_path, comparison, value)
        attribute_query = common_mongo_query.build_string_criteria("{}.#text".format(
            element_path), comparison, value)

    key, value = element_query.popitem()
    element_query_key = {'path': "/.*{}/".format(key)}
    element_query_value = {'value': value}
    element_query = common_mongo_query.build_and_criteria(element_query_key, element_query_value)

    key, value = attribute_query.popitem()
    attribute_query_key = {'path': "/.*{}/".format(key)}
    attribute_query_value = {'value': value}
    attribute_query = common_mongo_query.build_and_criteria(attribute_query_key,
                                                            attribute_query_value)

    criteria = common_mongo_query.build_or_criteria(element_query, attribute_query)

    if is_not:
        return common_mongo_query.invert_query(criteria)
    else:
        return criteria
