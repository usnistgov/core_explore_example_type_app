"""Url router for the REST API
"""
from django.conf.urls import url
from core_explore_example_type_app.rest.query import views as query_views

urlpatterns = [
    url(r'^local-query-data-item', query_views.ExecuteLocalQueryDataItemView.as_view(),
        name='core_explore_example_type_local_query_data_item')
]
