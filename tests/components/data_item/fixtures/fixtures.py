""" Fixtures files for Data Item
"""
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_explore_example_type_app.components.data_item.models import DataItem, Item
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace


class DataItemFixtures(FixtureInterface):
    """ Data Item fixtures
    """

    data_1 = None
    data_2 = None
    template = None
    data_collection = None
    data_item_collection = list()

    def insert_data(self):
        """ Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_data_collection()
        self.generate_data_item_collection()

    def generate_data_collection(self):
        """ Generate a Data collection.

        Returns:

        """
        # NOTE: no xml_content to avoid using unsupported GridFS mock
        self.data_1 = Data(
            template=self.template, user_id="1", dict_content=None, title="title"
        ).save()
        self.data_2 = Data(
            template=self.template, user_id="2", dict_content=None, title="title2"
        ).save()
        self.data_collection = [self.data_1, self.data_2]

    def generate_template(self):
        """ Generate an unique Template.

        Returns:

        """
        template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        template.content = xsd
        template.hash = ""
        template.filename = "filename"
        self.template = template.save()

    def generate_data_item_collection(self):
        """ Generate a Data collection.

        Returns:

        """
        data_item_collection = list()

        for data in self.data_collection:
            data_item = DataItem(
                data=data,
                template=data.template,
                list_content=[Item(path="dummy.path", value="value")],
                last_modification_date=data.last_modification_date,
            ).save()
            data_item_collection.append(data_item)

        self.data_item_collection = data_item_collection


class AccessControlDataItemFixture(FixtureInterface):
    """ Access Control Data Item fixture
    """

    USER_1_NO_WORKSPACE = 0
    USER_2_NO_WORKSPACE = 1
    USER_1_WORKSPACE_1 = 2
    USER_2_WORKSPACE_2 = 3

    template = None
    workspace_1 = None
    workspace_2 = None
    data_collection = None
    data_item_collection = list()
    data_user_1 = list()
    data_user_2 = list()

    def insert_data(self):
        """ Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_workspace()
        self.generate_data_collection()
        self.generate_data_item_collection()

    def generate_data_collection(self):
        """ Generate a Data collection.

        Returns:

        """
        data_1 = Data(template=self.template, title="Data 1", user_id="1").save()
        self.data_user_1.append(data_1)
        data_2 = Data(template=self.template, title="Data 2", user_id="2").save()
        self.data_user_2.append(data_2)
        data_3 = Data(
            template=self.template,
            title="Data 3",
            user_id="1",
            workspace=self.workspace_1.id,
        ).save()
        self.data_user_1.append(data_3)
        data_4 = Data(
            template=self.template,
            title="Data 4",
            user_id="2",
            workspace=self.workspace_2.id,
        ).save()
        self.data_user_2.append(data_4)
        self.data_collection = [data_1, data_2, data_3, data_4]

    def generate_template(self):
        """ Generate an unique Template.

        Returns:

        """
        template = Template()
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element name="tag"></xs:element></xs:schema>'
        )
        template.content = xsd
        template.hash = ""
        template.filename = "filename"
        self.template = template.save()

    def generate_workspace(self):
        """ Generate an unique Template.

        Returns:

        """
        self.workspace_1 = Workspace(
            title="Workspace 1", owner="1", read_perm_id="1", write_perm_id="1"
        ).save()
        self.workspace_2 = Workspace(
            title="Workspace 2", owner="2", read_perm_id="2", write_perm_id="2"
        ).save()

    def generate_data_item_collection(self):
        """ Generate a Data collection.

        Returns:

        """
        data_item_collection = list()

        for data in self.data_collection:
            data_item = DataItem(
                data=data,
                template=data.template,
                list_content=[Item(path="dummy.path", value="value")],
                last_modification_date=data.last_modification_date,
            ).save()
            data_item_collection.append(data_item)

        self.data_item_collection = data_item_collection
