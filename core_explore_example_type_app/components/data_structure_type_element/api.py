"""API for Data Structure Type Element
"""
from core_explore_example_type_app.components.data_structure_type_element.models import (
    DataStructureTypeElement,
)


def upsert(data_structure_type_element):
    """ Save or update the Data Structure Type Element

    Args:
        data_structure_type_element:

    Returns: DataStructureTypeElement object.

    """
    return data_structure_type_element.save_object()


def get_by_data_structure_id(data_structure_id):
    """ Get Data structure type element object which contains the given data_structure id

    Args:
        data_structure_id:

    Returns: DataStructureTypeElement object

    """
    return DataStructureTypeElement.get_by_data_structure_id(data_structure_id)


def get_by_id(data_structure_type_element_id):
    """ Return DataStructureTypeElement object with the given id

        Args:
            data_structure_type_element_id:

        Returns: DataStructureTypeElement object
    """
    return DataStructureTypeElement.get_by_id(data_structure_type_element_id)
