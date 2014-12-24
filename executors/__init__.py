import copy
import logging
import pkgutil
import re
from errors import InitializationError

__author__ = 'corvis'

_EXPRESSION_REGEX = re.compile('\$(?P<name>\w[\d\w]*)(?P<is_func>\((?P<arg>.*?)?\))?')


class Executor(object):
    name = None

    def __init__(self):
        self.__interpolation_map = {}

    @classmethod
    def build_from_def(cls, ref_name, definition):
        instance = cls(ref_name, definition)
        return instance

    def preprocess_user_object(self, obj, context=None):
        """
        Applies expression processor on each field of the given object.
        It returns brand new object instead of modifying the input.
        :param obj: object to be processed
        :type obj: dict
        :param context: local context to be used for interpolation
        :return:
        """
        res = copy.copy(obj)
        for key in res:
            if isinstance(res[key], basestring):
                res[key] = self.user_value(res[key], context)
        return res

    def user_value(self, value, context=None):
        """
        This method should be applied on each user string to make expression resolver work.
        It returns an input value replacing all expressions on actual values
        :param value:
        :param context:
        :return:
        """
        # only strings are supported at this point
        if not isinstance(value, basestring):
            return value
        if context is None:
            context = {}
        result = value
        # check if given value contains expressions
        match = _EXPRESSION_REGEX.search(result)
        while match is not None:
            expression_value = None
            # try to find value or callable in interpolation map
            expression_name = match.group('name')
            if expression_name not in self.__interpolation_map:
                raise Exception('Expression {} is not allowed in this context'.format(expression_name))
            value_or_callable = self.__interpolation_map.get(expression_name)
            # is it value-expression
            if match.group('is_func') is None and not callable(value_or_callable):
                raise Exception('Expression {0} should not be a function. Use ${0} syntax without brackets.'.format(match.group('name')))
            if callable(value_or_callable):
                argument = self.user_value(match.group('arg'), context)     # apply interpolation on the argument
                expression_value = str(value_or_callable(argument, context))
            else:
                expression_value = str(value_or_callable)

            result = result.replace(match.group(0), expression_value, 1)
            match = _EXPRESSION_REGEX.search(result)
        return result

    def initialize_context(self, configuration, system_state):
        """
        This methods should be overridden in child class.
        It will be invoked before execute method to register all required context variables and functions.
        Implementation should use self.register_preprocessor to register needed data in context.
        :return:
        """
        pass

    def register_preprocessor(self, name, value_or_callable):
        self.__interpolation_map[name] = value_or_callable

    def execute(self, configuration, system_state):
        """
        :type configuration: domain.Configuration
        :type system_state: domain.SystemState
        :return:
        """
        self.initialize_context(configuration, system_state)


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