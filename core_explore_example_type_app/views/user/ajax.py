"""Explore Example Type app Ajax views
"""
import json

from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest

import core_explore_example_app.permissions.rights as rights
import core_main_app.utils.decorators as decorators
from core_explore_example_app.components.explore_data_structure import api as \
    explore_data_structure_api
from core_explore_example_type_app.utils.parser.parser import render_form, generate_element_absent,\
    generate_choice_absent, remove_form_element
from core_main_app.components.template import api as template_api


@decorators.permission_required(content_type=rights.explore_example_content_type,
                                permission=rights.explore_example_access, raise_exception=True)
def load_form(request):
    """ Load the form

    Args:
        request:

    Returns:

    """
    try:
        template_id = request.POST['templateID']
        template = template_api.get(template_id)
        # get data structure
        data_structure = explore_data_structure_api.create_and_get_explore_data_structure(request,
                                                                                          template,
                                                                                          request.user.id)
        root_element = data_structure.data_structure_element_root

        # renders the form
        xsd_form = render_form(request, root_element)
        response_dict = {'xsd_form': xsd_form}
        return HttpResponse(json.dumps(response_dict), content_type='application/json')
    except Exception, e:
        return HttpResponseBadRequest("An error occurred while generating the form.")


@decorators.permission_required(content_type=rights.explore_example_content_type,
                                permission=rights.explore_example_access, raise_exception=True)
def generate_element(request):
    """Generate an element absent from the form.

    Args:
        request:

    Returns:

    """
    try:
        element_id = request.POST['id']
        html_form = generate_element_absent(request, element_id)
    except Exception, e:
        return HttpResponseBadRequest()

    return HttpResponse(html_form)


@decorators.permission_required(content_type=rights.explore_example_content_type,
                                permission=rights.explore_example_access, raise_exception=True)
def generate_choice(request):
    """Generate a choice branch absent from the form.

    Args:
        request:

    Returns:

    """
    try:
        element_id = request.POST['id']
        html_form = generate_choice_absent(request, element_id)
    except Exception, e:
        return HttpResponseBadRequest()

    return HttpResponse(html_form)


@decorators.permission_required(content_type=rights.explore_example_content_type,
                                permission=rights.explore_example_access, raise_exception=True)
def remove_element(request):
    """Remove an element from the form.

    Args:
        request:

    Returns:

    """
    element_id = request.POST['id']
    code, html_form = remove_form_element(request, element_id)
    return HttpResponse(json.dumps({'code': code, 'html': html_form}))