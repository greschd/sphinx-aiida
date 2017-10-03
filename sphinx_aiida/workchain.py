"""
Defines an rst directive to auto-document AiiDA workchains.
"""

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
        workchain_name = self.arguments[0]
        module_name, class_name = workchain_name.rsplit('.', 1)
        workchain = load_class(workchain_name)

        workchain_node = addnodes.desc(
            desctype='class', domain='py', noindex=False, objtype='class'
        )
        signature = addnodes.desc_signature(first=False, fullname="Workchain")
        signature += addnodes.desc_annotation(text='workchain')
        signature += addnodes.desc_addname(text=module_name + '.')
        signature += addnodes.desc_name(text=class_name)
        workchain_node += signature

        print(workchain.spec().get_inputs_template())
        return [workchain_node]


# def process_aiida_workchains(app, doctree, fromdocname):
