import copy
import re
from profileconf import global_context
from profileconf.domain import ContextFunction

__author__ = 'corvis'

_EXPRESSION_REGEX = re.compile('\$(?P<name>\w[\d\w]*)(?P<is_func>\((?P<arg>.*?)?\))?')


class ContextSupport(object):
    def __init__(self):
        self.__interpolation_map = {}

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
            context_function = self.__interpolation_map.get(expression_name)
            # is it value-expression
            if not isinstance(context_function, ContextFunction):
                raise Exception(
                    'Expression "{0}" can \'t be evaluated. "{0}" doesn\'t exist in this context'.format(match.group(0),
                                                                                                         match.group(
                                                                                                             'name')))
            argument = self.user_value(match.group('arg'), context)  # apply interpolation on the argument
            expression_value = context_function.invoke(argument, context)
            if len(result) == len(match.group(0)):
                result = expression_value
                break
            else:
                result = result.replace(match.group(0), str(expression_value), 1)
            match = _EXPRESSION_REGEX.search(result)
        return result

    def initialize_context(self, configuration=None, system_state=None):
        """
        This methods should be overridden in child class.
        It will be invoked before execute method to register all required context variables and functions.
        Implementation should use self.register_preprocessor to register needed data in context.
        :return:
        """
        pass

    def initialize_global_context(self, configuration=None, system_state=None):
        # Restricted collections
        self.register_context_function(global_context.all)
        self.register_context_function(global_context.one_of)
        self.register_context_function(global_context.only)

    def register_context_function(self, context_function):
        assert isinstance(context_function, ContextFunction)
        self.__interpolation_map[context_function.name] = context_function