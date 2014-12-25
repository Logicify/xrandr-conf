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

    def system_state_detector(self):
        return self.__system_state_detector


class Screen(object):

    def __init__(self):
        self.name = None
        self.id = None
        self.displays = []

    def __str__(self):
        return 'Screen {0}'.format(self.id)

    def __unicode__(self):
        return self.__str__()

    def get_active_displays(self):
        return [x for x in self.displays if x.is_active]

    def get_connected_displays(self):
        return [x for x in self.displays if x.is_connected]

    def get_displays_by_wildcard(self, wildcard):
        res = []
        for x in self.displays:
            if wildcard.strip() == '*' or x.id == wildcard:
                res.append(x)
        return res

    def get_display(self, id):
        """
        Get display by id
        :param id:
        :rtype: Display
        """
        for x in self.displays:
            if x.id == id:
                return x
        return None


class Display(object):

    def __init__(self):
        self.id = None
        self.is_connected = False
        self.primary = False
        self.resolution = None
        self.position = (0, 0)
        self.modes = []
        self.preferred_mode = None
        self.current_mode = None

    @property
    def is_active(self):
        return self.resolution is not None

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return 'Display {0}: connected={1}, active={4}, primary={2}, resolution={3}'.format(self.id, self.is_connected,
                                                                                  self.primary, self.resolution,
                                                                                  self.is_active)


class DisplayMode(object):
    def __init__(self):
        self.resolution = None
        self.rate = None
        self.is_preferred = False
        self.is_activated = False

    def __str__(self):
        return '{} rate {}Hz{}'.format(self.resolution, self.rate, ' (preferred)' if self.is_preferred else '')

    def __unicode__(self):
        return self.__str__()


class SystemState(object):
    def __init__(self):
        self.screens = []

    @property
    def default_screen(self):
        """
        :rtype: Screen
        """
        if len(self.screens) == 0:
            return None
        return self.screens[0]


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