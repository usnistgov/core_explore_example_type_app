""" Explore example type tasks
"""
import logging

from celery import shared_task

import core_explore_example_type_app.system.api as system_data_item_api
import core_main_app.system.api as data_system_api
from core_main_app.components.data.models import Data
from core_main_app.settings import DATA_SORTING_FIELDS

logger = logging.getLogger(__name__)


@shared_task
def generate_data_items_from_all_data_in_database():
    """ Generate DataItem from all data in db
    """
    try:

        data = Data.get_all(DATA_SORTING_FIELDS)
        for document in data:
            try:
                logger.info("START processing data : %s" % document.id)
                system_data_item_api.upsert_from_data(document, force_update=False)
            except Exception as e:
                logger.error(
                    "ERROR : Impossible to init the DataItem data : %s" % str(e)
                )
        logger.info("All data items are created")
    except Exception as e:
        logger.error("ERROR : Impossible to init the DataItems : %s" % str(e))


@shared_task
def generate_data_items_from_data(data_id):
    """ Generate DataItem from data
    """
    try:
        data = data_system_api.get_data_by_id(data_id)
        logger.info("START processing data : %s" % data_id)
        system_data_item_api.generate_data_items_from_data(data)
        logger.info("All data items are created")
    except Exception as e:
        logger.error("ERROR : Impossible to init the DataItem data : %s" % str(e))
