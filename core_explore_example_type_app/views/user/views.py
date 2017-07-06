"""Explore example type user views
"""
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query

from core_explore_example_app.views.user.views import BuildQueryView
from core_main_app.components.template import api as template_api


class TypeBuildQueryView(BuildQueryView):
    build_query_url = 'core_explore_example_type_build_query'
    get_query_url = 'core_explore_example_type_get_query'
    results_url = 'core_explore_example_type_results'
    object_name = "type"

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
