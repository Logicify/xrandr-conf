from profileconf.domain import SystemState
from profileconf.repository import ApplicationContext

__author__ = 'corvis'


class SystemStateDetector(object):
    def capture_system_state(self):
        """
        :rtype: SystemStateSection
        """
        pass

# class Detector(object):
#
#     def get_pulseaudio_state(self):
#         pa = PulseAudio('profile-conf')
#         try:
#             pa.connect()
#             server_info = pa.get_server_info()
#             cards_info = pa.get_card_info_list()
#             sources_info = pa.get_source_info_list()
#             modules_info = pa.get_module_info_list()
#             sink_info = pa.get_sink_info_list()
#             pa.load_module
#         except:
#             pass
#         finally:
#             pa.disconnect()
#
#     def capture_system_state(self):
#         """
#         :rtype: domain.Detector
#         """
#         system_state = SystemState()
#         #system_state.screens = self.get_connected_screens()
#         self.get_pulseaudio_state()
#         exit()
#         return system_state


def capture_system_state():
    system_state = SystemState()
    for module in ApplicationContext().get().modules:
        if module.system_state_detector is not None:
            section = module.system_state_detector().capture_system_state()
            system_state.add_section(section)
    return system_state