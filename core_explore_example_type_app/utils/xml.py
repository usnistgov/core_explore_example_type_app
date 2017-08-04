"""
    Xml utils provide tool operation for data items.
"""
from core_main_app.utils.xml import convert_value

# FIXME: Add unit tests
def generate_items(element, path):
    """ Recursive method generating item.

    Args:
        element:
        path:

    Returns: List [{path, value}, ...]

    """
    # Counter on the sibling element names
    counters = {}
    items_list = []

    # if the node contains a value
    if element is not None and (hasattr(element, "text") and element.text is not None):
        text = element.text.strip()
        # Several lines ?
        lines = text.splitlines()

        if len(lines) > 1:
            # could calculate an index here
            for line in lines:
                item = {'path': path, 'value': convert_value(line)}
                items_list.append(item)
        else:
            item = {'path': path, 'value': convert_value(text)}
            items_list.append(item)

    # Loop on child elements
    for child in element:
        tag = child.tag

        # Print child node recursively
        items_list.extend(generate_items(child, "{0}.{1}".format(path, tag)))

    return items_list
