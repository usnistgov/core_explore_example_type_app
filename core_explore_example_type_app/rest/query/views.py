""" REST views for the query API
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core_explore_common_app.utils.query.mongo.query_builder import QueryBuilder
from core_explore_common_app.rest.query.views import process_data_list
from core_explore_example_type_app.components.data_item import api as data_item_api


@api_view(['GET'])
def execute_local_query_data_item(request):
    """Executes query on local instance (data items) and returns results

    Args:
        request:

    Returns:

    """
    try:
        # get query
        query = request.data.get('query', None)

        if query is not None:
            # build query builder
            query_builder = QueryBuilder(query, "list_content")
            # get raw query
            raw_query = query_builder.get_raw_query()
            # execute query
            data_list = data_item_api.execute_query(raw_query, "data")
            return process_data_list(request, data_list)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
