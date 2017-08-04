"""Url router for the REST API
"""
from django.conf.urls import url
from core_explore_example_type_app.rest.query import views as query_views

urlpatterns = [
    url(r'^local-query-data-item', query_views.execute_local_query_data_item,
        name='core_explore_example_type_local_query_data_item')
]
