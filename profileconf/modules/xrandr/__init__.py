from profileconf.domain import Module
from profileconf.modules.xrandr.conditions import MonitorConnectedCondition
from profileconf.modules.xrandr.executors import XrandrExecutor, ConfigureDisplaysExecutor
from profileconf.modules.xrandr.state_detector import DisplayStateDetector

__author__ = 'corvis'


class XrandrModule(Module):
    def __init__(self):
        super(XrandrModule, self).__init__()
        self.name = "xrandr"
        self.description = "Utilize display management capabilities"
        self.set_system_state_detector(DisplayStateDetector)
        self.add_condition_handler(MonitorConnectedCondition)
        self.add_executor(XrandrExecutor)
        self.add_executor(ConfigureDisplaysExecutor)
