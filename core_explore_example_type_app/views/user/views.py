"""Explore example type user views
"""
from core_composer_app.components.type import api as type_api
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query
from core_explore_example_app.views.user.views import IndexView, BuildQueryView
from core_main_app.components.template import api as template_api


class TypeIndexView(IndexView):

    def __init__(self, **kwargs):
        super(TypeIndexView, self).__init__(**kwargs)
        # Get a list of complex_type ids
        self.list_complex_type_ids = [str(complex_type.id) for complex_type in
                                      type_api.get_all_complex_type()]

    def get_global_active_list(self):
        """ Get global version managers having a current type of type definition complexType.

        Args:

        Returns:
            List of global version managers.

        """
        global_active_list = super(TypeIndexView, self).get_global_active_list()
        # Filter only complex_type
        global_active_list = global_active_list.filter(current__in=self.list_complex_type_ids)

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
        # Filter only complex_type
        user_active_list = user_active_list.filter(current__in=self.list_complex_type_ids)

        return user_active_list


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
    def _get_css():
        base_css = super(TypeBuildQueryView, TypeBuildQueryView)._get_css()
        # Add custom css
        base_css.extend(["core_explore_example_type_app/user/css/query_builder_type.css",])
        return base_css

    @staticmethod
    def _create_new_query(user_id, type_):
        """ Create a new query
        Args:
            user_id:
            type_:

        """
        # Get templates using the given Type
        # Here we should get all dependencies recurcively and remove all template.type from the list
        # Passing an empty list is a quick fix
        # templates = template_api.get_all_templates_by_dependencies([type_])
        # Create query
        query = Query(user_id=str(user_id), templates=[])
        return query_api.upsert(query)
