""" Unit Test Data
"""
from core_main_app.utils.integration_tests.integration_base_test_case import \
    MongoIntegrationBaseTestCase
from tests.components.data_item.fixtures.fixtures import DataItemFixtures
from core_explore_example_type_app.components.data_item.models import DataItem
from core_main_app.commons import exceptions
from bson.objectid import ObjectId

fixture_data = DataItemFixtures()


class TestDataGetByData(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_data_get_by_data_raises_api_error_if_not_found(self):
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            DataItem.get_by_data(ObjectId())

    def test_data_get_by_data_return_data_if_found(self):
        # Act
        result = DataItem.get_by_data(self.fixture.data_1.id)
        # Assert
        self.assertEqual(result.data, self.fixture.data_1)
