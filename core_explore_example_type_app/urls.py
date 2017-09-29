""" Url router for the explore example application
"""

from core_composer_app.components.type_version_manager import api as type_version_manager_api
from django.conf.urls import url, include

from core_explore_example_app.views.user import views as explore_example_app_user_views
from core_explore_example_app.views.user import ajax as explore_example_app_user_ajax
from core_explore_example_type_app.utils.mongo_query import fields_to_query
from core_explore_example_type_app.views.user import views as user_views
from core_explore_example_type_app.views.user import ajax as user_ajax

urlpatterns = [
    url(r'^rest/', include('core_explore_example_type_app.rest.urls')),

    url(r'^$', user_views.
        TypeIndexView.as_view(api=type_version_manager_api,
                              object_name="type",
                              select_object_redirect="core_explore_example_type_select_fields",
                              build_query_redirect="core_explore_example_type_build_query"),
        name='core_explore_example_type_index'),

    url(r'^load-form$', user_ajax.load_form,
        name='core_explore_example_type_load_form'),

    url(r'^generate-element$', user_ajax.generate_element,
        name='core_explore_example_type_generate_element'),

    url(r'^generate-choice$', user_ajax.generate_choice,
        name='core_explore_example_type_generate_choice'),

    url(r'^remove-element$', user_ajax.remove_element,
        name='core_explore_example_type_remove_element'),

    url(r'^select-fields/(?P<template_id>\w+)$',
        explore_example_app_user_views.
        SelectFieldsView.as_view(build_query_url="core_explore_example_type_build_query",
                                 load_form_url='core_explore_example_type_load_form',
                                 generate_element_url='core_explore_example_type_generate_element',
                                 remove_element_url='core_explore_example_type_remove_element',
                                 generate_choice_url='core_explore_example_type_generate_choice'),
        name='core_explore_example_type_select_fields'),

    url(r'^build-query/(?P<template_id>\w+)$',
        user_views.TypeBuildQueryView.as_view(),
        name='core_explore_example_type_build_query'),

    url(r'^build-query/(?P<template_id>\w+)/(?P<query_id>\w+)$',
        user_views.TypeBuildQueryView.as_view(),
        name='core_explore_example_type_build_query'),

    url(r'^results/(?P<template_id>\w+)/(?P<query_id>\w+)$',
        explore_example_app_user_views.ResultQueryView.as_view(
            back_to_query_redirect='core_explore_example_type_build_query'),
        name='core_explore_example_type_results'),

    url(r'^get-query$', explore_example_app_user_ajax.GetQueryView.as_view(
        fields_to_query_func=fields_to_query),
        name='core_explore_example_type_get_query'),

    url(r'^save-query$', explore_example_app_user_ajax.SaveQueryView.as_view(
        fields_to_query_func=fields_to_query),
        name='core_explore_example_type_save_query'),
]
