""" Data items model
"""
from django_mongoengine import fields, Document, EmbeddedDocument
from mongoengine import errors as mongoengine_errors
from mongoengine.queryset.base import CASCADE

from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template


class Item(EmbeddedDocument):
    """ Item object
    """
    path = fields.StringField(blank=False)
    value = fields.DynamicField(blank=False)


class DataItem(Document):
    """ Data Item object
    """
    # When data is deleted, all relative data item is deleted as well
    data = fields.ReferenceField(Data, blank=False, reverse_delete_rule=CASCADE)
    template = fields.ReferenceField(Template, blank=False)
    list_content = fields.ListField(fields.EmbeddedDocumentField(Item), default=[], blank=False)
    last_modification_date = fields.DateTimeField(blank=True, default=None)

    @staticmethod
    def get_by_data(data):
        """ Return a Data Item with the data given.

        Args:
            data:

        Returns:

        """
        try:
            return DataItem.objects(data=data).get()
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    @staticmethod
    def delete_from_data(data):
        """ Delete data items relative to the given data

        Args:
            data:

        Returns:

        """
        DataItem.objects(data=data).delete()

    @staticmethod
    def execute_query(query, distinct_field):
        """Execute a query.

        Args:
            query:
            distinct_field:

        Returns:

        """
        return DataItem.objects(__raw__=query).distinct(distinct_field)
