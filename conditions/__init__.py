import logging
import pkgutil
from errors import InitializationError

__author__ = 'corvis'


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


class ConditionsRegistry(object):
    def __init__(self):
        self.conditions = {}
        self.__logger = logging.getLogger('ConditionsRegistry')

    def register(self, condition_cls):
        if condition_cls.name in self.conditions:
            raise InitializationError('This condition processor({}) is already registered'.format(condition_cls.name))
        if not issubclass(condition_cls, Condition):
            raise InitializationError('Only subclasses of Condition can be registered')
        condition_name = condition_cls.name
        self.conditions[condition_name] = condition_cls
        # Register all aliases
        for alias in condition_cls.aliases:
            self.conditions[alias] = condition_cls
        self.__logger.info('Registered condition class "{}"'.format(condition_name))

    def create_condition(self, condition_name, condition_def):
        if condition_name not in self.conditions:
            raise InitializationError('Unknown condition \"{}\"'.format(condition_name))
        condition_cls = self.conditions[condition_name]
        return condition_cls.build_from_def(condition_name, condition_def)

    def autodiscover(self):
        __all__ = []
        for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
            __all__.append(module_name)
            __import__('.'.join((__name__, module_name)), globals(), locals())


registry = ConditionsRegistry()