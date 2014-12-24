import subprocess
import re
from domain import Screen, Display, SystemState, DisplayMode

__author__ = 'corvis'


class Detector(object):
    __REGEX_SCREEN_LINE = re.compile('Screen (?P<id>\d+)')
    __REGEX_DISPLAY_LINE = re.compile('(?P<id>[\w\d]+) (?P<con>connected|disconnected)\s?(?P<primary>primary)?\s?((?P<resolution>\d+x\d+)?\+(?P<left>\d+)\+(?P<top>\d+))?')
    __REGEX_MODE_LINE = re.compile('\s+(?P<resolution>\d+x\d+)\s+(?P<rate>\d+\.\d+)\s*(?P<mod>[+\*]+)?')

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
                current_display.resolution = match.group('resolution')
                current_display.position = (match.group('left'), match.group('top'))
                current_screen.displays.append(current_display)
            # check if it is resolution line
            match = self.__REGEX_MODE_LINE.match(line)
            if match is not None:
                mode = DisplayMode()
                current_display.modes.append(mode)
                mode.resolution = match.group('resolution')
                mode.rate = match.group('rate')
                modifiers = match.group('mod')
                if modifiers is not None:
                    mode.is_preferred = '+' in modifiers
                    mode.is_activated = '*' in modifiers
                    if mode.is_activated:
                        current_display.current_mode = mode
                    if mode.is_preferred:
                        current_display.preferred_mode = mode
        return devices

    def capture_system_state(self):
        """
        :rtype: domain.Detector
        """
        system_state = SystemState()
        system_state.screens = self.get_connected_screens()
        return system_state