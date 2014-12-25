from profileconf.domain import Module

__author__ = 'corvis'


class PulseAudioModule(Module):
    def __init__(self):
        super(PulseAudioModule, self).__init__()
        self.name = "pulseaudio"