import logging
import imp
from profileconf.condition import Condition
from profileconf.domain import Module
from profileconf.errors import InitializationError
from profileconf.executor import Executor
import os

__author__ = 'corvis'


class ExecutorsRegistry(object):
    def __init__(self):
        self.executors = {}
        self.__logger = logging.getLogger('Bootstrap')

    def register(self, executor_cls):
        if executor_cls.name in self.executors:
            raise InitializationError('This executor ({}) is already registered'.format(executor_cls.name))
        if not issubclass(executor_cls, Executor):
            raise InitializationError('Only subclasses of Executor can be registered')
        executor_name = executor_cls.name
        self.executors[executor_name] = executor_cls
        self.__logger.info(' --> Registered executor "{}"'.format(executor_name))

    def create_executor(self, executor_name, executor_def):
        if executor_name not in self.executors:
            raise InitializationError('Unknown executor \"{}\"'.format(executor_name))
        condition_cls = self.executors[executor_name]
        return condition_cls.build_from_def(executor_name, executor_def)


class ConditionsRegistry(object):
    def __init__(self):
        self.conditions = {}
        self.__logger = logging.getLogger('Bootstrap')

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
        self.__logger.info(' --> Registered condition handler "{}"'.format(condition_name))

    def create_condition(self, condition_name, condition_def):
        if condition_name not in self.conditions:
            raise InitializationError('Unknown condition handler \"{}\"'.format(condition_name))
        condition_cls = self.conditions[condition_name]
        return condition_cls.build_from_def(condition_name, condition_def)


class ApplicationContext(object):
    __instance = None

    @classmethod
    def get(cls):
        """
        :rtype: ApplicationContext
        """
        if ApplicationContext.__instance is None:
            ApplicationContext.__instance = ApplicationContext()
        return ApplicationContext.__instance

    def __init__(self):
        self.conditions_repository = ConditionsRegistry()
        self.executors_repository = ExecutorsRegistry()
        self.modules = []
        self.__logger = logging.getLogger('Bootstrap')

    def load_module(self, path):
        split_path = path.split('/')
        module_name = split_path[-1]
        imported_package = imp.load_package(module_name, path)
        module = None
        for name, cls in imported_package.__dict__.items():
            if isinstance(cls, type) and issubclass(cls, Module) and cls != Module:
                module = cls()
                break
        if module is None:
            raise InitializationError("Unable to load module \"{}\" ({})".format(module_name, path))
        self.__logger.info("Loading module {} ...".format(module.name if module is not None else module_name))
        # Construct the class and load module
        self.modules.append(module)
        for x in module.condition_handlers:
            self.conditions_repository.register(x)
        for x in module.executors:
            self.executors_repository.register(x)
        if module.system_state_detector is not None:
            self.__logger.info(' --> Registered system state detector: {}'.format(module.system_state_detector.__name__))
        self.__logger.info("Module loaded: {}".format(module.name if module is not None else module_name))
        return True

    def bootstrap(self):
        self.__logger.info('Initializing built-in modules...')
        standard_modules_path = os.path.join(os.path.dirname(__file__), 'modules')
        # Check each dir in modules folder
        loaded_modules_count = 0
        subdirectories = os.walk(standard_modules_path).next()[1]
        try:
            for x in subdirectories:
                if self.load_module(os.path.join(standard_modules_path, x)):
                    loaded_modules_count += 1
            self.__logger.info('{} built-in modules initialized'.format(loaded_modules_count))
        except InitializationError as e:
            self.__logger.error("Unable to load some of the module(-es): " + e.message)
            self.__logger.exception(e)
            raise e
        return True
