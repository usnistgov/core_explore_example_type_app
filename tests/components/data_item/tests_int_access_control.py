""" Access control testing
"""
from mock.mock import patch

from core_explore_example_type_app.components.data_item import api as data_item_api
from core_main_app.components.data.models import Data
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.components.data_item.fixtures.fixtures import AccessControlDataItemFixture

fixture_data = AccessControlDataItemFixture()


class TestDataExecuteQuery(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    # FIXME update test
    # @patch(
    #     "core_main_app.components.workspace.api"
    #     ".get_all_workspaces_with_read_access_by_user"
    # )
    # def test_execute_query_distinct_by_data_returns_data(self, get_all):
    #     mock_user = _create_user("3")
    #     get_all.return_value = [fixture_data.workspace_1]
    #     data_item_list = data_item_api.execute_query_distinct_by_data({}, mock_user)
    #     self.assertTrue(len(data_item_list) > 0)
    #     self.assertTrue(all(isinstance(data, Data) for data in data_item_list))

    # FIXME update test
    # @patch(
    #     "core_main_app.components.workspace.api"
    #     ".get_all_workspaces_with_read_access_by_user"
    # )
    # def test_execute_query_distinct_by_data_returns_data_in_workspace_1(self, get_all):
    #     mock_user = _create_user("3")
    #     get_all.return_value = [fixture_data.workspace_1]
    #     data_item_list = data_item_api.execute_query_distinct_by_data({}, mock_user)
    #     self.assertTrue(len(data_item_list) == 1)
    #     self.assertTrue(data_item.data.workspace == "1" for data_item in data_item_list)

    # FIXME update test
    # @patch(
    #     "core_main_app.components.workspace.api"
    #     ".get_all_workspaces_with_read_access_by_user"
    # )
    # def test_execute_query_distinct_by_data_returns_data_in_workspace_2(self, get_all):
    #     mock_user = _create_user("3")
    #     get_all.return_value = [fixture_data.workspace_1]
    #     data_item_list = data_item_api.execute_query_distinct_by_data({}, mock_user)
    #     self.assertTrue(len(data_item_list) == 1)
    #     self.assertTrue(data_item.data.workspace == "2" for data_item in data_item_list)

    # FIXME update test
    # @patch(
    #     "core_main_app.components.workspace.api"
    #     ".get_all_workspaces_with_read_access_by_user"
    # )
    # def test_execute_query_distinct_by_data_returns_data_in_workspace_1_and_2(
    #     self, get_all
    # ):
    #     mock_user = _create_user("3")
    #     get_all.return_value = [fixture_data.workspace_1, fixture_data.workspace_2]
    #     data_item_list = data_item_api.execute_query_distinct_by_data({}, mock_user)
    #     self.assertTrue(len(data_item_list) == 2)
    #     self.assertTrue(
    #         data_item.data.workspace == "1" or data_item.data.workspace == "2"
    #         for data_item in data_item_list
    #     )

    def test_execute_query_distinct_by_data_as_superuser_returns_all_data(self):
        mock_user = _create_user("1", is_superuser=True)
        data_item_list = data_item_api.execute_query_distinct_by_data({}, mock_user)
        self.assertTrue(len(data_item_list) == 4)


def _create_user(user_id, is_superuser=False):
    return create_mock_user(user_id, is_superuser=is_superuser)
