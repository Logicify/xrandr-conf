__author__ = 'corvis'


class Module(object):
    def __init__(self):
        self.__system_state_detector = None
        self.__config_parser = None
        self.__condition_handlers = []
        self.__executors = []
        self.name = None
        self.description = None


    # TODO: Type validation!

    def set_system_state_detector(self, detector_cls):
        self.__system_state_detector = detector_cls

    def set_config_parser(self, parser_cls):
        self.__config_parser = parser_cls

    def add_condition_handler(self, condition_cls):
        self.__condition_handlers.append(condition_cls)

    def add_executor(self, condition_cls):
        self.__executors.append(condition_cls)

    @property
    def condition_handlers(self):
        return self.__condition_handlers

    @property
    def executors(self):
        return self.__executors

    @property
    def config_parser(self):
        return self.__config_parser

    @property
    def system_state_detector(self):
        """
        :rtype: SystemStateDetector
        """
        return self.__system_state_detector


class SystemStateSection(object):
    def __init__(self):
        self.name = None


class SystemState(object):
    def __init__(self):
        self.__sections = {}

    def get_section(self, name):
        """
        Returns configuration section by name
        :param name:
        :return:
        """
        return self.__sections.get(name)

    def add_section(self, section):
        if not isinstance(section, SystemStateSection):
            raise Exception('Section should be an instance of SystemStateSection')
        if section.name is None:
            raise Exception('Section name is not defined')
        self.__sections[section.name] = section

    def iter(self):
        return self.__sections.iteritems()


class Profile(object):
    def __init__(self):
        self.conditions = []
        self.id = None
        self.name = None
        self.keywords = []
        self.executors = []

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return 'Profile \"{}\"'.format(self.verbose_name)

    @property
    def verbose_name(self):
        return (self.name if self.name is not None else self.id)


class ContextFunction(object):

    class __ContextFunctionBuilder(object):

        def __init__(self):
            self.__context_function = ContextFunction(None)

        def set_name(self, name):
            self.__context_function.name = name
            return self

        def set_description(self, name):
            self.__context_function.name = name
            return self

        def set_context_tag(self, context_tag):
            self.__context_function.context_tag = context_tag
            return self

        def returns_const_value(self, value):
            self.__context_function.set_callable(value)
            return self

        def set_handler(self, callable):
            self.__context_function.set_callable(callable)
            return self

        def build(self):
            if self.__context_function.name is None:
                raise ValueError('Context function should have a name')
            return self.__context_function

    @classmethod
    def builder(cls):
        return cls.__ContextFunctionBuilder()

    def __init__(self, name, value_or_callable=None, description=None):
        super(ContextFunction, self).__init__()
        self.name = None
        self.description = None
        self.context_tag = None
        self.__callable = value_or_callable

    def set_callable(self, value_or_callable):
        if callable(value_or_callable):
            self.__callable = value_or_callable
        else:
            self.__callable = lambda argument, context: value_or_callable

    def invoke(self, argument, context):
        return self.__callable(argument, context)


class Configuration(object):

    def __init__(self):
        self.profiles = {}
        self.executors = {}


class RestrictedList(list):
    ANY_OF = 0
    ALL = 1
    ONLY = 2

    def __init__(self, iterable=None, restriction=None):
        super(RestrictedList, self).__init__(iterable if iterable is not None else [])
        self.restriction = (restriction if restriction is not None else RestrictedList.ALL)

    def match(self, collection):
        """
        Detects if this list matches given collection.
        :param collection:
        :return:
        """
        if self.restriction == RestrictedList.ALL:
            for x in self:
                if x not in collection:
                    return False
            return True
        elif self.restriction == RestrictedList.ANY_OF:
            for x in self:
                if x in collection:
                    return True
            return False
        elif self.restriction == RestrictedList.ONLY:
            if len(collection) != len(self):
                return False
            for x in collection:
                if x not in self:
                    return False
            return True
        return False