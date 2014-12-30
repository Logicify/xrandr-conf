import logging
import time
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
    __time_tracking_logger = logging.getLogger('TimeTracking')
    start_time = time.time()
    system_state = SystemState()
    for module in ApplicationContext().get().modules:
        if module.system_state_detector is not None:
            section = module.system_state_detector().capture_system_state()
            system_state.add_section(section)
    execution_time = time.time() - start_time
    __time_tracking_logger.info('Captured system state in {}ms'.format(int(round(execution_time * 1000))))
    return system_state