""" System API data item
"""

from django.http import HttpRequest
from xml_utils.xsd_tree.xsd_tree import XSDTree

import core_explore_example_type_app.components.data_item.api as data_item_api
import core_main_app.commons.exceptions as exceptions
from core_explore_example_type_app.components.data_item.models import Item, DataItem
from core_explore_example_type_app.utils.parser.parser import get_parser
from core_explore_example_type_app.utils.parser.renderer.xml_type import XmlTypeRenderer
from core_explore_example_type_app.utils.xml import generate_items
from core_parser_app.components.data_structure_element import api as data_structure_element_api
from core_parser_app.tools.parser.parser import delete_branch_from_db


def generate_data_items_from_data(data):
    """ Generate all data items structure.

    Args:
        data:

    Returns:

    """
    try:
        # In case we are editing a data, need to delete old items relative to it
        data_item_api.delete_from_data_if_exists(data)

        # build data_structure
        root_element = _generate_form(data.template.content, data.xml_content)
        # build XML renderer and get xml
        xml_data = XmlTypeRenderer(root_element).render()

        # build tree and get the root
        root = XSDTree.build_tree(xml_data).getroot()

        # generate item from the root
        generated_items = generate_items(root, root.tag)
        list_to_insert = []
        for generated_item in generated_items:
            item = Item(path=generated_item['path'], value=generated_item['value'])
            list_to_insert.append(item)

        # Upsert DataItem
        data_item = DataItem(data=data, template=data.template, list_content=list_to_insert,
                             last_modification_date=data.last_modification_date)
        data_item_api.upsert(data_item)

        # delete data_structure
        delete_branch_from_db(root_element.id)
    except Exception, e:
        raise exceptions.ApiError('An error occurred during the generation: {0}.'.format(e.message))


def upsert_from_data(data, force_update=False):
    """ Create or Update a DataItem from a Data document.
    Args:
        data: Data document
        force_update: Force the Update of the DataItem.

    Returns:

    """
    try:
        data_item = data_item_api.get_by_data(data)
        # Check if the document that we have needs to be updated.
        if data_item.last_modification_date != data.last_modification_date or force_update:
            generate_data_items_from_data(data)
    except exceptions.DoesNotExist:
        generate_data_items_from_data(data)
    except Exception, e:
        raise e


def _generate_form(xsd_string, xml_string):
    """Generate the form using the parser, returns the root element.

    Args:
        xsd_string:
        xml_string:

    Returns:

    """
    # build parser
    parser = get_parser()
    # generate form
    root_element_id = parser.generate_form(xsd_string, xml_string)
    # get the root element
    root_element = data_structure_element_api.get_by_id(root_element_id)

    return root_element
