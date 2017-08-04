"""Explore Example type app Ajax views
"""

import json

from xml_utils.xsd_tree.operations.namespaces import get_namespaces, get_default_prefix

import core_explore_example_app.permissions.rights as rights
import core_main_app.utils.decorators as decorators
from core_explore_example_app.utils import mongo_query as common_mongo_query
from core_explore_example_type_app.utils import mongo_query as custom_mongo_query
from core_explore_example_app.utils.query_builder import get_element_value, get_element_comparison
from core_main_app.components.template import api as template_api


@decorators.permission_required(content_type=rights.explore_example_content_type,
                                permission=rights.explore_example_access,
                                raise_exception=True)
def fields_to_query(request, form_values, template_id):
    """Takes values from the html tree and creates a query from them

    Args:
        request:
        form_values:
        template_id:

    Returns:

    """

    # FIXME: Get rid of sessions
    map_criteria = request.session['mapCriteriaExplore']

    query = dict()
    for field in form_values:
        bool_comp = field['operator']
        is_not = bool_comp == 'NOT'

        # get element value
        value = get_element_value(field)
        # get comparison operator
        comparison = get_element_comparison(field)

        # get data structures for query
        criteria_info = json.loads(map_criteria[field['id']])
        element_info = json.loads(criteria_info['elementInfo']) if criteria_info[
                                                                       'elementInfo']is not None else None
        query_info = json.loads(criteria_info['queryInfo']) if criteria_info[
                                                                   'queryInfo'] is not None else None

        element_type = element_info['type']
        if element_type == "query":
            query_value = query_info['query']
            criteria = common_mongo_query.build_query_criteria(query_value, is_not)
        elif element_type == "enum":
            element = element_info['path']
            criteria = custom_mongo_query.build_enum_criteria(element, value, is_not)
        else:
            element = element_info['path']
            template = template_api.get(template_id)
            namespaces = get_namespaces(template.content)
            default_prefix = get_default_prefix(namespaces)
            criteria = custom_mongo_query.build_criteria(element, comparison, value,
                                                         element_type, default_prefix, is_not)

        if bool_comp == 'OR':
            query = common_mongo_query.build_or_criteria(query, criteria)
        elif bool_comp == 'AND':
            query = common_mongo_query.build_and_criteria(query, criteria)
        else:
            if form_values.index(field) == 0:
                query.update(criteria)
            else:
                query = common_mongo_query.build_and_criteria(query, criteria)

    return query
