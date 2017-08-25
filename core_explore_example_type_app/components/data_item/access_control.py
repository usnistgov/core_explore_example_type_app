""" Set of functions to define the rules for access control
"""

from core_workspace_app.components.workspace import api as workspace_api

from django.conf import settings


def get_user_readable_data_item_query(func, query, user):
    """ Get user readable data_item, given a query.

    Args:
        func:
        query:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(query, user)

    data_item_list = func(query, user)
    # Get a list of data item readable by the user.
    data_item_list = _get_user_readable_data_item_list(data_item_list, user)
    return data_item_list


def _get_user_readable_data_item_list(data_item_list, user):
    """ Return a list of data item readable by the user.

    Args:
        data_item_list:
        user:

    Returns:

    """
    if 'core_workspace_app' in settings.INSTALLED_APPS:
        filtered_data_item_list = []
        # get list of accessible workspaces
        accessible_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
        # FIXME: Beware of performance issue
        # Check that the data is owned by the user or if an accessible workspace
        for data_item in data_item_list:
            data = data_item.data
            if data.user_id == str(user.id) or data.workspace in accessible_workspaces:
                filtered_data_item_list.append(data_item)

        return filtered_data_item_list
    else:
        # general case: users can read other users data. Return a list and not a queryset.
        return list(data_item_list)
