"""Explore Example type app Ajax views
"""

import core_main_app.utils.decorators as decorators

import core_explore_example_app.permissions.rights as rights
from core_explore_example_app.views.user.ajax import get_query as example_get_query


@decorators.permission_required(content_type=rights.explore_example_content_type,
                                permission=rights.explore_example_access, raise_exception=True)
def get_query(request):
    """Get a query

    Args:
        request:

    Returns:

    """
    # FIXME: Has to be changed to build a query for the Type. Need to analyze this part.
    return example_get_query(request)