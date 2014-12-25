from profileconf.detector import SystemStateDetector
from profileconf.modules.pulseaudio.tools import PulseAudio

__author__ = 'corvis'


class PulseAudioStateDetector(SystemStateDetector):

    def get_pulseaudio_state(self):
        pa = PulseAudio('profile-conf')
        try:
            pa.connect()
            server_info = pa.get_server_info()
            cards_info = pa.get_card_info_list()
            sources_info = pa.get_source_info_list()
            modules_info = pa.get_module_info_list()
            sink_info = pa.get_sink_info_list()
            pa.load_module
        except:
            pass
        finally:
            pa.disconnect()

    def capture_system_state(self):
        return
