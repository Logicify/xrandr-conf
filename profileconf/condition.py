class Condition(object):
    name = None
    aliases = []

    @classmethod
    def build_from_def(cls, ref_name, definition):
        instance = cls(ref_name, definition)
        return instance

    def evaluate(self, current_system_state):
        """
        This method will be invoked on current system configuration.
        It should determine if system state matches this condition
        :param current_system_state:
        :return:
        """
        return False
