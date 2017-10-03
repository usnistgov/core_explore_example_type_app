""" Add Explore Example Type in main menu
"""

from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

# FIXME: CHECK AUTHENTICATION !
Menu.add_item(
    "main", MenuItem("Query by Type", reverse("core_explore_example_type_index"))
)
