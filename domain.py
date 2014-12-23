__author__ = 'corvis'


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
        self.resolution_line = None

    @property
    def is_active(self):
        return self.resolution_line is not None

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return 'Display {0}: connected={1}, active={4}, primary={2}, resolution={3}'.format(self.id, self.is_connected,
                                                                                  self.primary, self.resolution_line,
                                                                                  self.is_active)


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