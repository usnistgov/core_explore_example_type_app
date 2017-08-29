""" Set of functions to define the rules for access control
"""

from core_workspace_app.components.workspace import api as workspace_api

from django.conf import settings


def get_user_readable_data(func, query, user):
    """ Get user readable data, given a query.

    Args:
        func:
        query:
        user:

    Returns:

    """
    data_list = func(query, user)
    if user.is_superuser:
        return data_list

    # Get a list of data readable by the user.
    data_list = _get_user_readable_data_list(data_list, user)
    return data_list


def _get_user_readable_data_list(data_list, user):
    """ Return a list of data readable by the user.

    Args:
        data_list:
        user:

    Returns:

    """
    if 'core_workspace_app' in settings.INSTALLED_APPS:
        filtered_data_list = []
        # get list of accessible workspaces
        accessible_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
        # FIXME: Beware of performance issue
        # Check that the data is owned by the user or if an accessible workspace
        for data in data_list:
            if data.user_id == str(user.id) or data.workspace in accessible_workspaces:
                filtered_data_list.append(data)

        return filtered_data_list
    else:
        # general case: users can read other users data.
        return data_list
