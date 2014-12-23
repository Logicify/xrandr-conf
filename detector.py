import subprocess
import re
from domain import Screen, Display, SystemState

__author__ = 'corvis'


class Detector(object):
    __REGEX_SCREEN_LINE = re.compile('Screen (?P<id>\d+)')
    __REGEX_DISPLAY_LINE = re.compile('(?P<id>[\w\d]+) (?P<con>connected|disconnected)\s?(?P<primary>primary)?\s?(?P<resolution>\d+x\d+\+\d+\+\d+)?')

    def __init__(self,):
        self.xrandrExecutable = 'xrandr'

    def get_connected_screens(self):
        p = subprocess.Popen([self.xrandrExecutable, '-q'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        devices = []
        current_screen, current_display = None, None
        for line in p.stdout.readlines():
            # check if it is screen line
            match = self.__REGEX_SCREEN_LINE.match(line)
            if match is not None:
                current_screen = Screen()
                current_screen.id = match.group('id')
                devices.append(current_screen)
                continue
            # check if it is display definition line
            match = self.__REGEX_DISPLAY_LINE.match(line)
            if match is not None:
                current_display = Display()
                current_display.id = match.group('id')
                current_display.is_connected = match.group('con') == 'connected'
                current_display.primary = match.group('primary') is not None
                current_display.resolution_line = match.group('resolution')
                current_screen.displays.append(current_display)
        return devices

    def capture_system_state(self):
        """
        :rtype: domain.Detector
        """
        system_state = SystemState()
        system_state.screens = self.get_connected_screens()
        return system_state