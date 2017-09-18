"""Util to build queries for mongo db
"""

from core_explore_example_app.utils import mongo_query as common_mongo_query


def fields_to_query(form_values, template_id):
    """Takes values from the html tree and creates a query from them

    Args:
        form_values:
        template_id:

    Returns:

    """
    return common_mongo_query.fields_to_query(form_values, template_id, use_wildcard=True)

