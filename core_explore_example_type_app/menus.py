""" Add Explore Example Type in main menu
"""

from django.urls import reverse
from menu import Menu, MenuItem

# FIXME: CHECK AUTHENTICATION !
Menu.add_item(
    "explorer", MenuItem("Query by Type", reverse("core_explore_example_type_index"))
)
