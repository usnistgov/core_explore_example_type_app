""" Data structure type element model
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors
from mongoengine.queryset.base import CASCADE

from core_main_app.commons import exceptions
from core_parser_app.components.data_structure_element.models import (
    DataStructureElement,
)


class DataStructureTypeElement(Document):
    """Represents data structure type object"""

    path = fields.StringField(blank=True)
    data_structure = fields.ReferenceField(
        DataStructureElement, unique=True, reverse_delete_rule=CASCADE
    )

    @staticmethod
    def get_by_data_structure_id(data_structure_id):
        """ Returns the object with the given data_structure id.

        Args:
            data_structure_id:

        Returns:
            DataStructureTypeElement (obj): DataStructureTypeElement object with the given
            data_structure id.

        """
        try:
            return DataStructureTypeElement.objects.get(
                data_structure=str(data_structure_id)
            )
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_id(data_structure_type_id):
        """ Returns the object with the given id.

        Args:
            data_structure_type_id:

        Returns:
            DataStructureTypeElement (obj): DataStructureTypeElement object with the given id.

        """
        try:
            return DataStructureTypeElement.objects.get(pk=str(data_structure_type_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def save_object(self):
        """Custom save

        Returns:

        """
        try:
            return self.save()
        except mongoengine_errors.NotUniqueError as e:
            raise exceptions.NotUniqueError(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
