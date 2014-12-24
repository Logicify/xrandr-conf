import logging
import pkgutil
from errors import InitializationError

__author__ = 'corvis'


class Executor(object):
    name = None

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
        pass


class ExecutorsRegistry(object):
    def __init__(self):
        self.executors = {}
        self.__logger = logging.getLogger('ExecutorsRegistry')

    def register(self, executor_cls):
        if executor_cls.name in self.executors:
            raise InitializationError('This executor ({}) is already registered'.format(executor_cls.name))
        if not issubclass(executor_cls, Executor):
            raise InitializationError('Only subclasses of Executor can be registered')
        executor_name = executor_cls.name
        self.executors[executor_name] = executor_cls
        self.__logger.info('Registered executor class "{}"'.format(executor_name))

    def create_executor(self, executor_name, executor_def):
        if executor_name not in self.executors:
            raise InitializationError('Unknown executor \"{}\"'.format(executor_name))
        condition_cls = self.executors[executor_name]
        return condition_cls.build_from_def(executor_name, executor_def)

    def autodiscover(self):
        __all__ = []
        for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
            __all__.append(module_name)
            __import__('.'.join((__name__, module_name)), globals(), locals())


registry = ExecutorsRegistry()