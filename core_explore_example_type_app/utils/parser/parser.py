"""Parser util for explore_example_type app
"""
from core_parser_app.tools.parser.parser import XSDParser


def get_parser():
    """Load configuration for the parser.

    Returns:

    """
    return XSDParser(min_tree=False,
                     ignore_modules=True,
                     collapse=True,
                     auto_key_keyref=False,
                     implicit_extension_base=False,
                     download_dependencies=True,
                     store_type=True)
