from profileconf.domain import Module
from profileconf.modules.pulseaudio.state_detector import PulseAudioStateDetector

__author__ = 'corvis'


class PulseAudioModule(Module):
    def __init__(self):
        super(PulseAudioModule, self).__init__()
        self.name = "pulseaudio"
        self.description = "PulseAudio module"
        self.set_system_state_detector(PulseAudioStateDetector)