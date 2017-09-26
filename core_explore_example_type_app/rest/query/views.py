""" REST views for the query API
"""
from core_explore_common_app.rest.query.views import ExecuteLocalQueryView
from core_explore_example_type_app.components.data_item import api as data_item_api


class ExecuteLocalQueryDataItemView(ExecuteLocalQueryView):
    sub_document_root = None

    def execute_raw_query(self, raw_query):
        return data_item_api.execute_query_distinct_by_data(raw_query, self.request.user)