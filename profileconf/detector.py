from profileconf.domain import SystemState
from profileconf.repository import ApplicationContext

__author__ = 'corvis'


class SystemStateDetector(object):
    def capture_system_state(self):
        """
        :rtype: SystemStateSection
        """
        pass


def capture_system_state():
    system_state = SystemState()
    for module in ApplicationContext().get().modules:
        if module.system_state_detector is not None:
            section = module.system_state_detector().capture_system_state()
            system_state.add_section(section)
    return system_state