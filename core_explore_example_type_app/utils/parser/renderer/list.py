"""List Renderer class
"""
import logging

from core_parser_app.tools.modules.views.module import AbstractModule
from core_parser_app.tools.parser.renderer.list import AbstractListRenderer
from core_explore_example_type_app.components.data_structure_type_element.models import (
    DataStructureTypeElement,
)
from core_explore_example_type_app.components.data_structure_type_element import (
    api as data_structure_type_element_api,
)
from core_main_app.commons.exceptions import NotUniqueError

logger = logging.getLogger(__name__)


# FIXME: This renderer is based on the list renderer from the parser. Can be refactored.
class ListRenderer(AbstractListRenderer):
    """List Renderer class
    """

    def __init__(self, xsd_data, request):
        """Initializes List renderer object

        Args:
            xsd_data:
            request:
        """
        super(ListRenderer, self).__init__(xsd_data)
        self.request = request  # FIXME Find a way to avoid the use of request
        self.partial = False

    def render(self, partial=False, full_path=""):
        """Renders form as a list

        Args:
            partial:
            full_path:

        Returns:

        """
        html_content = ""
        self.partial = partial
        # If the tree is partial, retrieve the root path as prefix.
        if partial:
            element_id = self.data.options.get("real_root", None)
            if element_id is not None:
                prefix = data_structure_type_element_api.get_by_data_structure_id(
                    element_id
                ).path
                full_path = "{0}".format("/".join(prefix.split("/")[:-1]))

        if self.data.tag == "element":
            html_content += self.render_element(self.data, full_path)
        elif self.data.tag == "attribute":
            html_content += self.render_attribute(self.data, full_path)
        elif self.data.tag == "choice":
            html_content += self.render_choice(self.data, full_path)
        elif self.data.tag == "sequence":
            html_content += self.render_sequence(self.data, partial, full_path)
        else:
            message = "render: " + self.data.tag + " not handled"
            self.warnings.append(message)

        if not partial:
            return self._render_warnings() + self._render_ul(
                html_content, str(self.data.pk)
            )
        else:
            return html_content

    def render_element(self, element, full_path=""):
        """Renders an element

        Args:
            element:
            full_path:

        Returns:

        """
        children = {}
        child_keys = []
        children_number = 0

        for child in element.children:
            if child.tag == "elem-iter":
                children[child.pk] = child.children
                child_keys.append(child.pk)

                if len(child.children) > 0:
                    children_number += 1
            else:
                message = "render_element (iteration): " + child.tag + " not handled"
                self.warnings.append(message)

        final_html = ""

        # Buttons generation (render once, reused many times)
        add_button = False
        del_button = False

        if "max" in element.options:
            if children_number < element.options["max"] or element.options["max"] == -1:
                add_button = True

        if "min" in element.options:
            if children_number > element.options["min"]:
                del_button = True

        buttons = self._render_buttons(add_button, del_button)

        element_name = element.options["name"]

        if "label" in element.options and element.options["label"] != "":
            element_name = element.options["label"]

        # Check if the element is complexType or simpleType
        is_complex_or_simple_type = _is_complex_or_simple_type(children, child_keys)

        # Build path.
        full_path = _build_full_path(full_path, is_complex_or_simple_type, element)

        # Create the data_structure type
        _create_data_structure_type_element(full_path=full_path, data_structure=element)

        for child_key in child_keys:
            # li_class = ''
            # FIXME Use tuples instead
            sub_elements = []
            sub_inputs = []
            sub_buttons = []

            for child in children[child_key]:
                if child.tag == "complex_type":
                    sub_elements.append(self.render_complex_type(child, full_path))
                    sub_inputs.append(False)
                    sub_buttons.append(True)
                elif child.tag == "simple_type":
                    sub_elements.append(self.render_simple_type(child, full_path))
                    sub_inputs.append(True)
                    sub_buttons.append(True)
                elif child.tag == "input":
                    sub_elements.append(self._render_input(child))
                    sub_inputs.append(True)
                    sub_buttons.append(True)
                elif child.tag == "module":
                    sub_elements.append(self.render_module(child))
                    sub_inputs.append(False)
                    sub_buttons.append(not child.options["multiple"])
                else:
                    message = "render_element: " + child.tag + " not handled"
                    self.warnings.append(message)

            if children_number == 0:
                html_content = element_name + buttons
                li_class = "removed"
            else:
                li_class = str(element.pk)
                html_content = ""
                for child_index in xrange(len(sub_elements)):
                    html_buttons = buttons

                    if not sub_buttons[child_index]:
                        html_buttons = self._render_buttons(False, del_button)

                    if sub_inputs[child_index]:
                        html_content += (
                            element_name + sub_elements[child_index] + html_buttons
                        )
                    else:
                        html_content += (
                            self._render_collapse_button() + element_name + html_buttons
                        )
                        html_content += self._render_ul(sub_elements[child_index], None)

            # FIXME temp fix, do it in a cleaner way
            if self.partial and "real_root" in element.options:
                li_class = element.options["real_root"]

            final_html += self._render_li(html_content, li_class, child_key)

        return final_html

    def render_complex_type(self, element, full_path=""):
        """Renders a complex type

        Args:
            element:
            full_path:

        Returns:

        """
        html_content = ""

        attributes = []
        simple = False

        for child in element.children:
            if child.tag == "sequence":
                html_content += self.render_sequence(element=child, full_path=full_path)
            elif child.tag == "simple_content":
                simple = True
                html_content += self.render_simple_content(child, full_path)
            elif child.tag == "complex_content":
                html_content += self.render_complex_content(child, full_path)
            elif child.tag == "attribute":
                attributes.append(self.render_attribute(child, full_path))
            elif child.tag == "choice":
                html_content += self.render_choice(child, full_path)
            elif child.tag == "module":
                html_content += self.render_module(child)
            else:
                message = "render_complex_type: " + child.tag + " not handled"
                self.warnings.append(message)

        if len(attributes) > 0:
            html_content = self._render_list_attributes(
                attributes, html_content, simple
            )
        return html_content

    def render_attribute(self, element, full_path=""):
        """Renders an attribute

        Args:
            element:
            full_path:

        Returns:

        """
        children = {}
        child_keys = []
        children_number = 0

        for child in element.children:
            if child.tag == "elem-iter":
                children[child.pk] = child.children
                child_keys.append(child.pk)

                if len(child.children) > 0:
                    children_number += 1
            else:
                message = "render_attribute (iteration): " + child.tag + " not handled"
                self.warnings.append(message)

        final_html = ""

        # Buttons generation (render once, reused many times)
        add_button = False
        del_button = False

        if "max" in element.options:
            if children_number < element.options["max"] or element.options["max"] == -1:
                add_button = True

        if "min" in element.options:
            if children_number > element.options["min"]:
                del_button = True

        buttons = self._render_buttons(add_button, del_button)
        element_name = element.options["name"]

        if "label" in element.options and element.options["label"] != "":
            element_name = element.options["label"]

        for child_key in child_keys:
            sub_elements = []
            sub_inputs = []
            sub_buttons = []

            for child in children[child_key]:
                if child.tag == "simple_type":
                    sub_elements.append(self.render_simple_type(child, full_path))
                    sub_inputs.append(True)
                    sub_buttons.append(True)
                elif child.tag == "input":
                    sub_elements.append(self._render_input(child))
                    sub_inputs.append(True)
                    sub_buttons.append(True)
                elif child.tag == "module":
                    sub_elements.append(self.render_module(child))
                    sub_inputs.append(False)
                    sub_buttons.append(not child.options["multiple"])
                else:
                    message = "render_attribute: " + child.tag + " not handled"
                    self.warnings.append(message)

            if children_number == 0:
                html_content = element_name + buttons
                li_class = "removed"
            else:
                li_class = str(element.pk)
                html_content = ""
                for child_index in xrange(len(sub_elements)):
                    html_buttons = buttons
                    if not sub_buttons[child_index]:
                        html_buttons = self._render_buttons(False, del_button)

                    if sub_inputs[child_index]:
                        html_content += (
                            element_name + sub_elements[child_index] + html_buttons
                        )
                    else:
                        html_content += (
                            self._render_collapse_button() + element_name + html_buttons
                        )
                        html_content += self._render_ul(sub_elements[child_index], None)

            # FIXME temp fix, do it in a cleaner way
            if self.partial and "real_root" in element.options:
                li_class = element.options["real_root"]

            final_html += self._render_li(html_content, li_class, child_key)

        return final_html

    def render_sequence(self, element, force_full_display=False, full_path=""):
        """Renders a sequence

        Args:
            element:
            force_full_display:
            full_path:

        Returns:

        """
        children = {}
        child_keys = []
        children_number = 0

        for child in element.children:
            if child.tag == "sequence-iter":
                children[child.pk] = child.children
                child_keys.append(child.pk)

                if len(child.children) > 0:
                    children_number += 1
            else:
                message = "render_sequence (iteration): " + child.tag + " not handled"
                self.warnings.append(message)

        final_html = ""

        # Buttons generation (render once, reused many times)
        add_button = False
        del_button = False
        empty = False

        if "max" in element.options:
            if children_number < element.options["max"] or element.options["max"] == -1:
                add_button = True

        if "min" in element.options:
            if children_number > element.options["min"]:
                del_button = True

            # Case of an empty sequence (no children => nb < min)
            if children_number < element.options["min"]:
                empty = True

        if empty:  # Empty sequence string (no need to go further)
            return ""

        buttons = self._render_buttons(add_button, del_button)

        for child_key in child_keys:
            # li_class = ''
            sub_elements = []
            html_content = ""

            for child in children[child_key]:
                if child.tag == "element":
                    sub_elements.append(self.render_element(child, full_path))
                elif child.tag == "sequence":
                    sub_elements.append(
                        self.render_sequence(element=child, full_path=full_path)
                    )
                elif child.tag == "choice":
                    sub_elements.append(self.render_choice(child, full_path))
                else:
                    message = "render_attribute: " + child.tag + " not handled"
                    self.warnings.append(message)

            if children_number == 0:
                li_class = "removed"
            else:
                li_class = str(element.pk)

                for child_index in xrange(len(sub_elements)):
                    if (
                        children_number != 1
                        or element.options["min"] != 1
                        or force_full_display
                    ):
                        html_content += self._render_ul(sub_elements[child_index], None)
                    else:
                        html_content += sub_elements[child_index]

            # FIXME temp fix, do it in a cleaner way
            if self.partial and "real_root" in element.options:
                li_class = element.options["real_root"]

            if (
                children_number != 1
                or element.options["min"] != 1
                or force_full_display
            ):
                final_html += self._render_li(
                    self._render_collapse_button()
                    + "Sequence "
                    + buttons
                    + html_content,
                    li_class,
                    child_key,
                )
            else:
                final_html += html_content

        return final_html

    def render_choice(self, element, full_path=""):
        """Renders a choice

        Args:
            element:
            full_path:

        Returns:

        """
        # html_content = ''
        children = {}
        child_keys = []
        choice_values = {}
        children_number = 0

        for child in element.children:
            if child.tag == "choice-iter":
                children[child.pk] = child.children
                child_keys.append(child.pk)

                if len(child.children) > 0:
                    children_number += 1

                choice_values[child.pk] = child.value
            else:
                message = "render_choice (iteration): " + child.tag + " not handled"
                self.warnings.append(message)

        # Buttons generation (render once, reused many times)
        add_button = False
        del_button = False

        if "max" in element.options:
            if children_number < element.options["max"] or element.options["max"] == -1:
                add_button = True

        if "min" in element.options:
            if children_number > element.options["min"]:
                del_button = True

        buttons = self._render_buttons(add_button, del_button)

        final_html = ""
        item_number = 1

        # if root xsi:type
        if full_path == "":
            is_root = True
        else:
            is_root = False

        for iter_element in child_keys:
            sub_content = ""
            html_content = ""
            options = []

            for child in children[iter_element]:

                if is_root:
                    full_path = _build_full_path(full_path, True, child)

                element_html = ""
                is_selected_element = str(child.pk) == choice_values[iter_element]

                if child.tag == "element":
                    options.append(
                        (str(child.pk), child.options["name"], is_selected_element)
                    )
                    element_html = self.render_element(child, full_path)
                elif child.tag == "sequence":
                    options.append(
                        (
                            str(child.pk),
                            "Sequence " + str(item_number),
                            is_selected_element,
                        )
                    )
                    item_number += 1

                    element_html = self.render_sequence(
                        element=child, full_path=full_path
                    )
                elif child.tag == "simple_type":
                    options.append(
                        (str(child.pk), child.options["name"], is_selected_element)
                    )
                    element_html = self.render_simple_type(child, full_path)
                elif child.tag == "complex_type":
                    options.append(
                        (str(child.pk), child.options["name"], is_selected_element)
                    )
                    element_html = self.render_complex_type(child, full_path)
                else:
                    message = "render_choice: " + child.tag + " not handled"
                    self.warnings.append(message)

                if element_html != "":
                    sub_content += self._render_ul(
                        element_html, str(child.pk), (not is_selected_element)
                    )

            if children_number == 0:  # Choice has no child
                li_class = "removed"
                html_content = "Choice " + buttons
            else:  # Choice has children
                li_class = str(element.pk)

                # Choice contains only one element, we don't generate the select
                if len(children[iter_element]) == 1:
                    html_content += options[0][1] + sub_content
                else:  # Choice contains a list
                    html_content += (
                        "Choice "
                        + self._render_select(None, "choice", options)
                        + buttons
                    )
                    html_content += sub_content

            # FIXME temp fix, do it in a cleaner way
            if self.partial and "real_root" in element.options:
                li_class = element.options["real_root"]

            final_html += self._render_li(html_content, li_class, iter_element)

        return final_html

    def render_simple_content(self, element, full_path=""):
        """Renders a simple content

        Args:
            element:
            full_path:

        Returns:

        """
        html_content = ""

        for child in element.children:
            if child.tag == "extension":
                html_content += self.render_extension(child, full_path)
            elif child.tag == "restriction":
                html_content += self.render_restriction(child, full_path)
            else:
                message = "render_simple_content: " + child.tag + " not handled"
                self.warnings.append(message)

        return html_content

    def render_complex_content(self, element, full_path=""):
        """Renders a complex type

        Args:
            element:
            full_path:

        Returns:

        """
        html_content = ""

        for child in element.children:
            if child.tag == "extension":
                html_content += self.render_extension(child, full_path)
            elif child.tag == "restriction":
                html_content += self.render_extension(child, full_path)
            else:
                message = "render_complex_content: " + child.tag + " not handled"
                self.warnings.append(message)

        return html_content

    def render_simple_type(self, element, full_path=""):
        """Renders a simple type

        Args:
            element:
            full_path:

        Returns:

        """
        html_content = ""

        for child in element.children:
            if child.tag == "restriction":
                # TODO: Check that
                html_content += self.render_restriction(child, full_path)
            elif child.tag == "list":
                html_content += self._render_input(child)
            elif child.tag == "union":
                html_content += self._render_input(child)
            elif child.tag == "attribute":
                html_content += self.render_attribute(child, full_path)
            elif child.tag == "module":
                html_content += self.render_module(child)
            elif child.tag == "choice":
                html_content += self.render_choice(child, full_path)
            else:
                message = "render_simple_type: " + child.tag + " not handled"
                self.warnings.append(message)

        return html_content

    def render_extension(self, element, full_path=""):
        """Renders an extension

        Args:
            element:
            full_path:

        Returns:

        """
        html_content = ""

        attributes = []
        simple = True

        for child in element.children:
            if child.tag == "input":
                html_content += self._render_input(child)
            elif child.tag == "attribute":
                attributes.append(self.render_attribute(child, full_path))
            elif child.tag == "simple_type":
                html_content += self.render_simple_type(child, full_path)
            elif child.tag == "complex_type":
                simple = False
                html_content += self.render_complex_type(child, full_path)
            else:
                message = "render_extension: " + child.tag + " not handled"
                self.warnings.append(message)

        if len(attributes) > 0:
            html_content = self._render_list_attributes(
                attributes, html_content, simple
            )

        return html_content

    def render_restriction(self, element, full_path=""):
        """Renders a restriction

        Args:
            element:
            full_path:

        Returns:

        """
        options = []
        sub_html = ""

        for child in element.children:
            if child.tag == "enumeration":
                options.append((child.value, child.value, child.value == element.value))
            elif child.tag == "simple_type":
                sub_html += self.render_simple_type(child, full_path)
            elif child.tag == "input":
                sub_html += self._render_input(child)
            else:
                message = "render_restriction: " + child.tag + " not handled"
                self.warnings.append(message)

        if sub_html == "" or len(options) != 0:
            return self._render_select(element, "restriction", options)
        else:
            return sub_html

    def render_module(self, element):
        """Renders a module

        Args:
            element:

        Returns:

        """
        module_options = element.options
        module_url = module_options["url"]

        module_view = AbstractModule.get_module_view(module_url)

        module_request = self.request
        module_request.method = "GET"

        module_request.GET = {
            "module_id": element.pk,
            "url": module_url,
            "xsd_xpath": module_options["xpath"]["xsd"],
            "xml_xpath": module_options["xpath"]["xml"],
        }

        # if the loaded doc has data, send them to the module for initialization
        if module_options["data"] is not None:
            module_request.GET["data"] = module_options["data"]

        if module_options["attributes"] is not None:
            module_request.GET["attributes"] = module_options["attributes"]

        # renders the module
        return module_view(module_request).content.decode("utf-8")

    def _render_list_attributes(self, attributes, html_content, simple_element):
        """Renders attributes as a list

        Args:
            attributes:
            html_content:
            simple_element:

        Returns:

        """
        if simple_element:
            data = {"attributes_html": attributes}
            html_content += self._load_template("attributes", data)
        else:
            html_content = "".join(attributes) + html_content

        return html_content


def _is_complex_or_simple_type(children, element_child_keys):
    """Check if the element is complexType or simpleType.

    Args:
        children:
        element_child_keys:

    Returns:

    """
    is_complex_or_simple_type = False
    for child_key in element_child_keys:
        for child in children[child_key]:
            if child.tag == "complex_type" or child.tag == "simple_type":
                is_complex_or_simple_type = True
                break

    return is_complex_or_simple_type


def _build_full_path(full_path, is_complex_or_simple_type, element):
    """ Build the full_path.

   Args:
       full_path:
       is_complex_or_simple_type:
       element:

   Returns:

   """
    # If complexType or SimpleType, we get the type name.
    if (
        is_complex_or_simple_type
        and "type" in element.options
        and element.options["type"] is not None
    ):
        full_path += "/{0}".format(element.options["type"])
    # If not, use the element name.
    else:
        full_path += "/{0}".format(element.options["name"])

    return full_path


def _create_data_structure_type_element(full_path, data_structure):
    """ Create a data structure type.

    Args:
        full_path:
        data_structure:

    Returns:

    """
    try:
        data_structure_type = DataStructureTypeElement(
            path=full_path, data_structure=data_structure
        )
        data_structure_type_element_api.upsert(data_structure_type)
    except (NotUniqueError, Exception):
        pass
