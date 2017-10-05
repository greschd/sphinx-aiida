"""
Defines an rst directive to auto-document AiiDA workchains.
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
import aiida
aiida.try_load_dbenv()
from aiida.orm.data import Data
from aiida.work.process import PortNamespace
from plum.util import load_class
from plum.port import InputPort


def setup_aiida_workchain(app):
    app.add_directive('aiida-workchain', AiidaWorkchainDirective)


class AiidaWorkchainDirective(Directive):
    """
    Directive to auto-document AiiDA workchains.
    """
    required_arguments = 1
    HIDDEN_INPUTS_FLAG = 'hidden-inputs'
    option_spec = {HIDDEN_INPUTS_FLAG: directives.flag}
    has_content = False

    def run(self):
        self.load_workchain()
        return self.build_node_tree()

    def load_workchain(self):
        """Loads the workchain and sets up additional attributes."""
        # pylint: disable=attribute-defined-outside-init
        self.workchain_name = self.arguments[0]
        self.module_name, self.class_name = self.workchain_name.rsplit('.', 1)
        self.workchain = load_class(self.workchain_name)
        self.workchain_spec = self.workchain.spec()

    def build_node_tree(self):
        """Returns the docutils node tree."""
        workchain_node = addnodes.desc(
            desctype='class', domain='py', noindex=False, objtype='class'
        )
        workchain_node += self.build_signature()
        workchain_node += self.build_content()
        return [workchain_node]

    def build_signature(self):
        """Returns the signature of the workchain."""
        signature = addnodes.desc_signature(first=False, fullname="Workchain")
        signature += addnodes.desc_annotation(text='workchain')
        signature += addnodes.desc_addname(text=self.module_name + '.')
        signature += addnodes.desc_name(text=self.class_name)
        return signature

    def build_content(self):
        """
        Returns the main content (docstring, inputs, outputs) of the workchain documentation.
        """
        content = addnodes.desc_content()
        content += nodes.paragraph(text=self.workchain.__doc__)

        # field_list = nodes.field_list()
        # content += field_list

        content += self.build_inputs_field()
        # field_list += self.build_outputs_field()

        return content

    def build_inputs_field(self):
        """
        Returns the field describing the workchain inputs.
        """
        paragraph = nodes.paragraph()
        # paragraph += addnodes.literal_strong(text='Inputs')
        paragraph += addnodes.literal_strong(text='Inputs:')
        paragraph += self.build_portnamespace_doctree(
            self.workchain_spec.inputs
        )

        return paragraph

    def build_portnamespace_doctree(self, portnamespace):
        """
        Builds the doctree for a port namespace.
        """
        result = nodes.bullet_list(bullet='*')
        for name, port in sorted(portnamespace.items()):
            if name.startswith(
                '_'
            ) and self.HIDDEN_INPUTS_FLAG not in self.options:
                continue
            if name == 'dynamic':
                continue
            item = nodes.list_item()
            if isinstance(port, InputPort):
                item += self.build_port_paragraph(name, port)
            elif isinstance(port, PortNamespace):
                item += addnodes.literal_strong(
                    text='Namespace {}'.format(name)
                )
                item += self.build_portnamespace_doctree(port)
            else:
                raise NotImplementedError
            result += item
        return result

    def build_port_paragraph(self, name, port):
        """
        Build the paragraph that describes a single port.
        """
        paragraph = nodes.paragraph()
        paragraph += addnodes.literal_strong(text=name)
        paragraph += nodes.Text(', ')
        paragraph += nodes.emphasis(
            text=self.format_valid_types(port.valid_type)
        )
        paragraph += nodes.Text(', ')
        paragraph += nodes.Text('required' if port.required else 'optional')
        if port.help:
            paragraph += nodes.paragraph(text=port.help)

        return paragraph

    @staticmethod
    def format_valid_types(valid_type):
        if issubclass(valid_type, Data):
            return valid_type.__name__
        return str(tuple(t.__name__ for t in valid_type))
