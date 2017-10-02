"""
Defines reStructuredText directives to simplify documenting AiiDA and its plugins.
"""

__version__ = '0.0.0a1'

from . import workchain


def setup(app):
    """
    Setup function to add the extension classes / nodes to Sphinx.
    """
    app.add_node(workchain.AiidaWorkchain)

    app.add_directive('aiida-workchain', workchain.AiidaWorkchainDirective)

    # app.connect('doctree-resolved', process_aiida_workchains)
    # app.connect('env-purge-doc', purge_aiida_workchains)

    return {'version': __version__, 'parallel_read_safe': True}
