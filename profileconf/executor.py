from profileconf.common import ContextSupport

__author__ = 'corvis'


class Executor(ContextSupport):
    name = None

    def __init__(self):
        super(Executor, self).__init__()

    @classmethod
    def build_from_def(cls, ref_name, definition):
        instance = cls(ref_name, definition)
        return instance

    def execute(self, configuration, system_state):
        """
        :type configuration: domain.Configuration
        :type system_state: domain.SystemState
        :return:
        """
        self.initialize_global_context(configuration, system_state)
        self.initialize_context(configuration, system_state)