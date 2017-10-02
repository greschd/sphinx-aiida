"""
Defines an rst directive to auto-document AiiDA workchains.
"""

from docutils.parsers.rst import Directive
import sphinx


class AiidaWorkchain(sphinx.addnodes.desc):
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
