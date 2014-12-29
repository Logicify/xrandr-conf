import logging
from profileconf.detector import SystemStateDetector
from profileconf.modules.pulseaudio.domain import PulseAudioState, PulseAudioOutput, PulseAudioSource, PulseAudioPort
from profileconf.modules.pulseaudio.tools import PulseAudio

__author__ = 'corvis'


class PulseAudioStateDetector(SystemStateDetector):

    def __init__(self):
        super(PulseAudioStateDetector, self).__init__()
        self.__logger = logging.getLogger('PulseAudioStateDetector')

    def get_pulseaudio_state(self):
        pa = PulseAudio('profile-conf')
        state = PulseAudioState()
        try:
            pa.connect()
            server_info = pa.get_server_info()
            if (len(server_info) > 0):
                server_info = server_info[0]
                state.pulse_server = server_info['server_name']
                state.pulse_server_version = server_info['server_version']
            else:
                return state    # Looks like there is no pulseaudio server available
            cards_info = pa.get_card_info_list()
            sources_info = pa.get_source_info_list()
            sink_info = pa.get_sink_info_list()
            for sink in sink_info:
                output = PulseAudioOutput()
                output.name = sink['name']
                output.description = sink['desc']
                output.index = sink['index']
                output.is_muted = sink['mute']
                state.available_outputs.append(output)
                if server_info['default_sink_name'] == sink['name']:
                    state.default_output = output
                for sink_port in sink['ports']:
                    port = PulseAudioPort()
                    port.name = sink_port['name']
                    port.description = sink_port['desc']
                    port.priority = sink_port['priority']
                    port.is_available = sink_port['available']
                    output.ports.append(port)
                    if sink_port['name'] == sink['active_port']:
                        output.active_port = port
            for pa_source in sources_info:
                source = PulseAudioSource()
                source.name = pa_source['name']
                source.description = pa_source['desc']
                source.index = pa_source['index']
                source.is_muted = pa_source['mute']
                state.available_sources.append(source)
                if server_info['default_source_name'] == pa_source['name']:
                    state.default_source = source
                for source_port in pa_source['ports']:
                    port = PulseAudioPort()
                    port.name = source_port['name']
                    port.description = source_port['desc']
                    port.priority = source_port['priority']
                    port.is_available = source_port['available']
                    source.ports.append(port)
                    if source_port['name'] == pa_source['active_port']:
                        source.active_port = port
            return state
        except Exception as e:
            self.__logger.exception(e)
            raise e
        finally:
            pa.disconnect()

    def capture_system_state(self):
        return self.get_pulseaudio_state()
