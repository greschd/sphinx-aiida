"""
Defines an rst directive to auto-document AiiDA workchains.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
import sphinx

def setup(app):
    app.add_node(aiida_workchain)

    app.add_directive('aiida-workchain', AiidaWorkchainDirective)

    app.connect('doctree-resolved', process_aiida_workchains)
    # app.connect('env-purge-doc', purge_aiida_workchains)

    return {'version': _module_version, 'parallel_read_safe': True}


class AiidaWorkchain(nodes.General, nodes.Element, sphinx.addnodes.desc):
    pass


class AiidaWorkchainDirective(Directive):
    def run(self):
        # env = self.state.document.settings.env
        return [
            AiidaWorkchain(
                '',
                sphinx.addnodes.desc_signature_line('foo'),
                sphinx.addnodes.desc_content('bar')
            )
        ]

# def process_aiida_workchains(app, doctree, fromdocname):
