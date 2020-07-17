""" REST views for the query API
"""

import json

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils.html import escape
from django.urls import reverse

from core_explore_common_app.components.abstract_query.models import (
    Authentication,
    DataSource,
)
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.constants import LOCAL_QUERY_NAME
from core_explore_common_app.rest.query.views import ExecuteLocalQueryView
from core_explore_common_app.utils.query.query import get_local_query_absolute_url
from core_explore_example_type_app.components.data_item import api as data_item_api
from core_main_app.settings import DATA_SORTING_FIELDS


class ExecuteLocalQueryDataItemView(ExecuteLocalQueryView):
    sub_document_root = None

    def execute_raw_query(self, raw_query, order_by_field):
        return data_item_api.execute_query_distinct_by_data(
            raw_query, self.request.user
        )


def update_local_data_source(request):
    """ Ajax method to update query with local data source

    Args:
        request:

    Returns:

    """
    try:
        query_id = request.GET["query_id"]
        selected = json.loads(request.GET["selected"])

        # Get query from id
        query = query_api.get_by_id(query_id)

        if selected:
            # Local data source is selected, add it to the query as a data source
            local_name = LOCAL_QUERY_NAME
            local_query_url = request.build_absolute_uri(
                reverse("core_explore_example_type_local_query_data_item")
            )
            authentication = Authentication(type="session")
            data_source = DataSource(
                name=local_name,
                url_query=local_query_url,
                authentication=authentication,
                order_by_field=",".join(DATA_SORTING_FIELDS),
            )
            data_source = data_source
            query_api.add_data_source(query, data_source)
        else:
            # Local data source is not selected, remove it from the query
            local_query_url = get_local_query_absolute_url(request)
            data_source = query_api.get_data_source_by_name_and_url_query(
                query, LOCAL_QUERY_NAME, local_query_url
            )
            query_api.remove_data_source(query, data_source)

        return HttpResponse()
    except Exception as e:
        return HttpResponseBadRequest(escape(str(e)))
