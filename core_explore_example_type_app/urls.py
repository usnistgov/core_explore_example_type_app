""" Url router for the explore example application
"""

from core_composer_app.components.type_version_manager import api as type_version_manager_api
from django.conf.urls import url

from core_explore_example_app.views.user import views as explore_example_app_user_views
from core_explore_example_type_app.views.user import ajax as user_ajax
from core_explore_example_type_app.views.user import views as user_views

urlpatterns = [
    url(r'^$', explore_example_app_user_views.
        IndexView.as_view(api=type_version_manager_api,
                          object_name="type",
                          select_object_redirect="core_explore_example_type_select_fields"),
        name='core_explore_example_type_index'),

    url(r'^select-fields/(?P<template_id>\w+)$',
        explore_example_app_user_views.
        SelectFieldsView.as_view(build_query_url="core_explore_example_type_build_query"),
        name='core_explore_example_type_select_fields'),

    url(r'^build-query/(?P<template_id>\w+)$',
        user_views.TypeBuildQueryView.as_view(),
        name='core_explore_example_type_build_query'),

    url(r'^build-query/(?P<template_id>\w+)/(?P<query_id>\w+)$',
        user_views.TypeBuildQueryView.as_view(),
        name='core_explore_example_type_build_query'),

    url(r'^results/(?P<template_id>\w+)/(?P<query_id>\w+)$',
        explore_example_app_user_views.results,
        name='core_explore_example_type_results'),

    url(r'^get-query$', user_ajax.get_query,
        name='core_explore_example_type_get_query'),
]
