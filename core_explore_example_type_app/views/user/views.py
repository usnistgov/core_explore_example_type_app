"""Explore example type user views
"""
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query

from core_explore_example_app.views.user.views import IndexView, BuildQueryView
from core_main_app.components.template import api as template_api


class TypeIndexView(IndexView):
    def get_global_active_list(self):
        """ Get global version managers having a current type of type definition complexType.

        Args:

        Returns:
            List of global version managers.

        """
        global_active_list = super(TypeIndexView, self).get_global_active_list()
        self._remove_type_version_if_simple_type(global_active_list)

        return global_active_list

    def get_user_active_list(self, user_id):
        """ Get active version managers with given user id having a current type of type
        definition complexType.

        Args:
            user_id:

        Returns:
            List of global version managers with given user.

        """
        user_active_list = super(TypeIndexView, self).get_user_active_list(user_id)
        self._remove_type_version_if_simple_type(user_active_list)

        return user_active_list

    def _remove_type_version_if_simple_type(self, type_version_list):
        """ Remove type_version from the given list if the current type has a simpleType
        definition.

        Args:
            type_version_list: List of type version.

        Returns:

        """
        for type_version in type_version_list:
            type_ = template_api.get(type_version.current)
            if not type_.is_complex:
                type_version_list.remove(type_version)


class TypeBuildQueryView(BuildQueryView):
    build_query_url = 'core_explore_example_type_build_query'
    get_query_url = 'core_explore_example_type_get_query'
    save_query_url = 'core_explore_example_type_save_query'
    results_url = 'core_explore_example_type_results'
    select_fields_url = 'core_explore_example_type_select_fields'
    local_query_url = 'core_explore_example_type_local_query_data_item'
    object_name = "type"
    data_sources_selector_template = \
        'core_explore_example_type_app/user/selector/data_sources_selector.html'

    @staticmethod
    def _create_new_query(user_id, type_):
        """ Create a new query
        Args:
            user_id:
            type_:

        """
        # Get templates using the given Type
        templates = template_api.get_all_templates_by_dependencies([type_])
        # Create query
        query = Query(user_id=str(user_id), templates=templates)
        return query_api.upsert(query)
