from aiida.work.workchain import WorkChain


class DemoWorkChain(WorkChain):
    """
    A demo workchain to show how the workchain auto-documentation works.
    """

    @classmethod
    def define(cls, spec):
        super(DemoWorkChain, cls).define(spec)
