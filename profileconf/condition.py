from profileconf.common import ContextSupport


class Condition(ContextSupport):
    name = None
    aliases = []

    @classmethod
    def build_from_def(cls, ref_name, definition):
        instance = cls()
        instance.initialize_global_context()
        instance.initialize_context()
        instance.initialize(ref_name, instance.user_value(definition))
        return instance

    def initialize(self, ref_name, definition):
        """
        Put initialization logic here.
        DO NOT USE __init__
        :return:
        """
        pass

    def evaluate(self, current_system_state):
        """
        This method will be invoked on current system configuration.
        It should determine if system state matches this condition
        :param current_system_state:
        :return:
        """
        return False
