from unittest.case import TestCase

from bson.objectid import ObjectId
from mock.mock import patch

from core_explore_example_type_app.components.data_structure_type_element import (
    api as data_structure_type_element_api,
)
from core_explore_example_type_app.components.data_structure_type_element.models import (
    DataStructureTypeElement,
)
from core_main_app.commons import exceptions
from core_parser_app.components.data_structure_element.models import (
    DataStructureElement,
)


class TestDataStructureTypeUpsert(TestCase):
    def setUp(self):
        self.data_structure = _create_data_structure_data()

    @patch.object(DataStructureTypeElement, "save_object")
    def test_data_structure_type_data_upsert_returns_object(self, mock_save):
        # Arrange
        mock_save.return_value = self.data_structure

        # Act
        result = data_structure_type_element_api.upsert(self.data_structure)

        # Assert
        self.assertIsInstance(result, DataStructureTypeElement)

    @patch.object(DataStructureTypeElement, "save_object")
    def test_data_structure_type_upsert_raises_error_if_save_failed(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            data_structure_type_element_api.upsert(self.data_structure)


class TestDataStructureTypeElementGetById(TestCase):
    @patch.object(DataStructureTypeElement, "get_by_id")
    def test_get_by_id_returns_object(self, mock_get_by_id):
        # Arrange
        mock_data_structure = _create_data_structure_data()
        mock_data_structure.id = ObjectId()

        mock_get_by_id.return_value = mock_data_structure

        # Act
        result = data_structure_type_element_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, DataStructureTypeElement)

    @patch.object(DataStructureTypeElement, "get_by_id")
    def test_get_by_id_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            data_structure_type_element_api.get_by_id(mock_absent_id)

    @patch.object(DataStructureTypeElement, "get_by_id")
    def test_get_by_id_raises_exception_if_internal_error(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            data_structure_type_element_api.get_by_id(mock_absent_id)


class TestDataStructureTypeGetByDataStructureId(TestCase):
    def setUp(self):
        self.data_structure = _create_data_structure_data()

    @patch.object(DataStructureTypeElement, "get_by_data_structure_id")
    def test_get_by_data_returns_object(self, mock_get_by_data_structure_id):
        # Arrange
        mock_data_structure = _create_data_structure_data()

        mock_get_by_data_structure_id.return_value = mock_data_structure

        # Act
        result = data_structure_type_element_api.get_by_data_structure_id(ObjectId())

        # Assert
        self.assertIsInstance(result, DataStructureTypeElement)

    @patch.object(DataStructureTypeElement, "get_by_data_structure_id")
    def test_get_by_data_raises_exception_if_object_does_not_exist(
        self, mock_get_by_data
    ):
        # Arrange
        mock_absent_data = ObjectId()

        mock_get_by_data.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            data_structure_type_element_api.get_by_data_structure_id(mock_absent_data)

    @patch.object(DataStructureTypeElement, "get_by_data_structure_id")
    def test_get_by_data_raises_exception_if_internal_error(self, mock_get_by_data):
        # Arrange
        mock_absent_data = ObjectId()

        mock_get_by_data.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            data_structure_type_element_api.get_by_data_structure_id(mock_absent_data)


def _create_data_structure_data():
    """ Get an DataStructureTypeElement object.

    Returns:
        DataStructureTypeElement instance.

    """
    data_structure = DataStructureTypeElement()
    data_structure = _set_data_structure_fields(data_structure)

    return data_structure


def _set_data_structure_fields(data_structure):
    """ Set DataStructureTypeElement fields.

    Returns:
        DataStructureTypeElement with assigned fields.

    """
    data_structure.path = "dummy.path"
    data_structure.data_structure = DataStructureElement()

    return data_structure
