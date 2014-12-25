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
        self.name = None
        self.executors = []

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return 'Profile \"{}\"'.format(self.name)


class Configuration(object):

    def __init__(self):
        self.profiles = {}
        self.executors = {}