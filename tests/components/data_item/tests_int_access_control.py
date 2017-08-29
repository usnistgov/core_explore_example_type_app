""" Access control testing
"""
from core_explore_example_type_app.components.data_item import api as data_item_api
from core_explore_example_type_app.components.data_item.models import DataItem
from core_main_app.utils.integration_tests.integration_base_test_case import  \
    MongoIntegrationBaseTestCase
from core_main_app.utils.tests_tools.MockUser import MockUser
from tests.components.data_item.fixtures.fixtures import AccessControlDataItemFixture

fixture_data = AccessControlDataItemFixture()


class TestDataItemExecuteQuery(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_execute_query_distinct_by_data_returns_data_item(self):
        mock_user = _create_user('1')
        data_item_list = data_item_api.execute_query_distinct_by_data({}, mock_user)
        self.assertTrue(isinstance(data, DataItem) for data in data_item_list)

    def test_execute_query_distinct_by_data_returns_all_data(self):
        mock_user = _create_user('1')
        data_item_list = data_item_api.execute_query_distinct_by_data({}, mock_user)
        self.assertTrue(len(data_item_list) == 4)

    def test_execute_query_distinct_by_data_returns_other_users_data(self):
        mock_user = _create_user('1')
        query = {'data': {'$in': [data.id for data in self.fixture.data_user_2]}}
        data_item_list = data_item_api.execute_query_distinct_by_data(query, mock_user)
        self.assertTrue(len(data_item_list) == 2)
        self.assertTrue(data_item.data.user_id == '2' for data_item in data_item_list)

    def test_execute_query_distinct_by_data_as_superuser_returns_all_data(self):
        mock_user = _create_user('1', is_superuser=True)
        data_item_list = data_item_api.execute_query_distinct_by_data({}, mock_user)
        self.assertTrue(len(data_item_list) == 4)


def _create_user(user_id, is_superuser=False):
    return MockUser(user_id, is_superuser=is_superuser)
