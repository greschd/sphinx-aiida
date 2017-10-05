from aiida.work.workchain import WorkChain
from aiida.orm.data.base import Int, Float, Bool


class DemoWorkChain(WorkChain):
    """
    A demo workchain to show how the workchain auto-documentation works.
    """

    @classmethod
    def define(cls, spec):
        super(DemoWorkChain, cls).define(spec)

        spec.input('x', valid_type=Float, help='First input argument.')
        spec.expose_inputs(SubWorkChain, namespace='sub')


class SubWorkChain(WorkChain):
    """
    A sub-workchain, to show how port namespaces are handled.
    """

    @classmethod
    def define(cls, spec):
        super(SubWorkChain, cls).define(spec)

        spec.input(
            'y',
            valid_type=Int,
            help="The second, nested input.",
            required=False
        )
        spec.expose_inputs(NestedSubWorkChain, namespace='sub')


class NestedSubWorkChain(WorkChain):
    """
    A nested workchain, to show how second-level port namespaces are handled.
    """

    @classmethod
    def define(cls, spec):
        super(NestedSubWorkChain, cls).define(spec)

        spec.input(
            'z',
            valid_type=Bool,
            help="A third input variable, that is nested two levels deep."
        )
