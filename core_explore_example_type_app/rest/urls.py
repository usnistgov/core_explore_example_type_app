"""Url router for the REST API
"""
from django.urls import re_path
from core_explore_example_type_app.rest.query import views as query_views

urlpatterns = [
    re_path(
        r"^local-query-data-item",
        query_views.ExecuteLocalQueryDataItemView.as_view(),
        name="core_explore_example_type_local_query_data_item",
    ),
    re_path(
        r"^update-type-query-data-source",
        query_views.update_local_data_source,
        name="core_explore_example_type_query_data_source",
    ),
]
