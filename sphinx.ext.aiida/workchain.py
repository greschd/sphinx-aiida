from . import __version__ as _module_version


def setup(app):
    app.add_node(aiida_workchain)

    app.add_directive('aiida-workchain', AiidaWorkchainDirective)

    return {'version': _module_version, 'parallel_read_safe': True}
