from docutils import nodes
from docutils.parsers.rst import Directive

from . import __version__ as _module_version


def setup(app):
    app.add_node(aiida_workchain)

    app.add_directive('aiida-workchain', AiidaWorkchainDirective)

    app.connect('doctree-resolved', process_aiida_workchains)
    app.connect('env-purge-doc', purge_aiida_workchains)

    return {'version': _module_version, 'parallel_read_safe': True}


class aiida_workchain(nodes.General, nodes.Element):
    pass


class AiidaWorkchainDirective(Directive):
    def run(self):
        return [aiida_workchain('')]
