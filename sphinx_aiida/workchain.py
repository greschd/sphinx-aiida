"""
Defines an rst directive to auto-document AiiDA workchains.
"""

from docutils.parsers.rst import Directive

from sphinx import addnodes


def setup_aiida_workchain(app):
    app.add_directive('aiida-workchain', AiidaWorkchainDirective)


class AiidaWorkchainDirective(Directive):
    required_arguments = 1
    has_content = False

    def run(self):
        workchain_node = addnodes.desc(
            desctype='class', domain='py', noindex=False, objtype='class'
        )
        signature = addnodes.desc_signature(first=False, fullname="Workchain")
        signature += addnodes.desc_annotation(text='workchain')
        signature += addnodes.desc_addname(text='foo.bar.')
        signature += addnodes.desc_name(text='Baz')
        workchain_node += signature
        # workchain_node += nodes.title(_('Foo'), _('bar'))

        return [workchain_node]


# def process_aiida_workchains(app, doctree, fromdocname):
