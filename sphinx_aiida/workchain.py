"""
Defines an rst directive to auto-document AiiDA workchains.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx import addnodes
import aiida
aiida.try_load_dbenv()
from plum.util import load_class


def setup_aiida_workchain(app):
    app.add_directive('aiida-workchain', AiidaWorkchainDirective)


class AiidaWorkchainDirective(Directive):
    """
    Directive to auto-document AiiDA workchains.
    """
    required_arguments = 1
    optional_arguments = 0
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
        return content


# def process_aiida_workchains(app, doctree, fromdocname):
