"""
Defines an rst directive to auto-document AiiDA workchains.
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
import aiida
aiida.try_load_dbenv()
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
        paragraph += addnodes.literal_strong(text='Inputs')
        paragraph += self.build_portnamespace_doctree(
            self.workchain_spec.inputs
        )

        return paragraph

    def build_portnamespace_doctree(self, portnamespace):
        result = nodes.bullet_list(bullet='*')
        for name, port in portnamespace.items():
            if name.startswith(
                '_'
            ) and self.HIDDEN_INPUTS_FLAG not in self.options:
                continue
            item = nodes.list_item()
            if isinstance(port, InputPort):
                item += self.build_port_paragraph(name, port)
            else:
                item += addnodes.literal_strong(
                    text='Namespace {}'.format(name)
                )
                item += self.build_portnamespace_doctree(port)
            result += item
        return result

    @staticmethod
    def build_port_paragraph(name, port):
        paragraph = nodes.paragraph()
        paragraph += addnodes.literal_strong(text=name)

        return paragraph
