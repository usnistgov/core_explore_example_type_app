"""XML Type Renderer class
"""
from core_parser_app.tools.parser.exceptions import RendererError
from core_parser_app.tools.parser.renderer.xml import XmlRenderer, get_parent_element


# FIXME: Refactor XmlRenderer to avoid duplicate code
class XmlTypeRenderer(XmlRenderer):
    """XML Type Renderer class
    """

    def render_element(self, element):
        """Render an element

        Args:
            element:

        Returns:

        """
        xml_string = ''
        children = {}
        child_keys = []
        children_number = 0

        for child in element.children:
            if child.tag == 'elem-iter':
                children[child.pk] = child.children
                child_keys.append(child.pk)

                if len(child.children) > 0:
                    children_number += 1
            else:
                message = 'render_element (iteration): ' + child.tag + ' not handled'
                self.warnings.append(message)

        for child_key in child_keys:
            for child in children[child_key]:
                content = ['', '', '']

                element_name = element.options['name']

                # add XML Schema instance prefix if root
                if self.isRoot:
                    xsi = ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                    content[0] += xsi
                    self.isRoot = False

                if child.tag == 'complex_type':
                    tmp_content = self.render_complex_type(child)
                    content[0] += tmp_content[0]
                    content[1] += tmp_content[1]
                    content[2] += tmp_content[2]
                    # Use the name of the type instead of the name of the element.
                    # element.options['type'] can appear and be equal to none
                    # that's why we don't do directly element_name = element.options['type']
                    if 'type' in element.options and element.options['type'] is not None:
                        element_name = element.options['type']
                elif child.tag == 'input':
                    tmp_content = child.value if child.value is not None else ''
                    content[1] += tmp_content
                elif child.tag == 'simple_type':
                    tmp_content = self.render_simple_type(child)
                    content[0] += tmp_content[0]
                    content[1] += tmp_content[1]
                    content[2] += tmp_content[2]
                    # Use the name of the type instead of the name of the element.
                    # element.options['type'] can appear and be equal to none
                    # that's why we don't do directly element_name = element.options['type']
                    if 'type' in element.options and element.options['type'] is not None:
                        element_name = element.options['type']
                elif child.tag == 'module':
                    tmp_content = self.render_module(child)

                    if child.options['multiple']:
                        content[2] += tmp_content[1]
                    else:
                        content[1] += tmp_content[1]
                else:
                    message = 'render_element: ' + child.tag + ' not handled'
                    self.warnings.append(message)

                # namespaces
                parent = get_parent_element(element)
                if parent is not None:
                    if 'xmlns' in element.options and element.options['xmlns'] is not None:
                        if 'xmlns' in parent.options and element.options['xmlns'] != parent.options['xmlns']:
                            xmlns = ' xmlns="{}"'.format(element.options['xmlns'])
                            content[0] += xmlns
                else:
                    if 'xmlns' in element.options and element.options['xmlns'] is not None:
                        xmlns = ' xmlns="{}"'.format(element.options['xmlns'])
                        content[0] += xmlns

                # content[2] has the value returned by a module (the entire tag, when multiple is True)
                if content[2] != '':
                    if content[0] != '' or content[1] != '':
                        raise RendererError('ERROR: More values than expected were returned (Module multiple).')
                    xml_string += content[2]
                else:
                    xml_string += self._render_xml(element_name, content[0], content[1])

        return xml_string
