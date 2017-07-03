"""Explore example type user views
"""
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query

from core_explore_example_app.views.user.views import BuildQueryView


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
        # create new query object
        # TODO: Get all templates using the type
        query = Query(user_id=str(user_id), templates=[type_])
        return query_api.upsert(query)
