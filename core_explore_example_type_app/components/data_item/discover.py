""" discover Data items for explore_example_type
"""
from core_explore_example_type_app.components.data_item import api as data_item_api
from core_main_app.components.data.models import Data


def generate_data_item_from_data():
    """ Check DataItem data information.
    """
    try:
        data = Data.get_all()
        for document in data:
            try:
                data_item_api.upsert_from_data(document, force_update=False)
            except Exception, e:
                print('ERROR : Impossible to init the DataItem data : %s' % e.message)
    except Exception, e:
        print('ERROR : Impossible to init the DataItems : %s' % e.message)
