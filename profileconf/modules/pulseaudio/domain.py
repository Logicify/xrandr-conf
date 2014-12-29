from profileconf.domain import SystemStateSection

__author__ = 'corvis'


class PulseAudioPort(object):

    def __init__(self):
        super(PulseAudioPort, self).__init__()
        self.name = None
        self.description = None
        self.priority = 0
        self.is_available = False

    def __str__(self):
        return "{}".format(self.description) + (" (unplugged)" if not self.is_available else "")

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()


class PulseAudioSource(object):
    def __init__(self):
        self.name = None
        self.index = None
        self.description = None
        self.is_muted = False
        self.ports = []
        self.active_port = None

    @property
    def is_monitor(self):
        return 'monitor' in self.name

    def __str__(self):
        return "{}".format(self.description) + (" (muted)" if self.is_muted else "")

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()


class PulseAudioOutput(object):
    def __init__(self):
        self.name = None
        self.index = None
        self.is_muted = False
        self.description = None
        self.ports = []
        self.active_port = None

    @property
    def is_monitor(self):
        return 'monitor' in self.name

    def __str__(self):
        return "{}".format(self.description) + (" (muted)" if self.is_muted else "")

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

class PulseAudioState(SystemStateSection):
    def __init__(self):
        super(PulseAudioState, self).__init__()
        self.name = 'pulseaudio'
        self.pulse_server = None
        self.pulse_server_version = None
        self.available_sources = []
        self.available_outputs = []
        self.default_output = None
        self.default_source = None

    def __str__(self):
        return "{}(outputs: {}, inputs: {})".format(self.pulse_server, len(self.available_outputs),
                                                    len(self.available_sources))

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()



