from . import Executor, registry
import subprocess
import re

__author__ = 'corvis'


class XrandrExecutor(Executor):
    name = "xrandr"

    def __init__(self, ref_name, definition):
        self.cmd_options = definition
        self.xrandrExecutable = 'xrandr'

    def execute(self, configuration, system_state):
        cmd_string = ' '.join([self.xrandrExecutable, self.cmd_options])
        p = subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        errors = '\n'.join(p.stderr.readline()).strip()
        res = p.stdout.readline()
        if len(errors) > 0:
            raise Exception(errors)
registry.register(XrandrExecutor)


class ConfigureDisplaysExecutor(Executor):
    name = "configure-displays"
    COORDS_REGEX = re.compile('^\d+x\d+$')
    DISPLAY_POSITION_REGEX = re.compile('(?P<location>left\-of|right\-of|below|above)\s+(?P<id>[\w\d]+)')

    def __init__(self, ref_name, definition):
        self.definition = definition

    def create_xrandr_screen_for_display(self, display, config_def):
        """
        See example definition for reference:
            state: "on"|"off"
            primary: true|false
            mode: "1920x1080"
            position: "0x0" | left-of <ID> | right-of <ID> | below <ID> | above <ID>
            rotate: "normal"
        :type display: domain.Display
        :param config_def:
        :return:
        """
        res = ['--output ' + display.id]
        if 'state' in config_def and config_def['state'].lower() == 'off':
            res.append('--off')
        if 'mode' in config_def:
            res.append('--mode ' + config_def['mode'])
        if 'position' in config_def:
            if self.COORDS_REGEX.match(config_def['position']):
                res.append('--pos ' + config_def['position'])
            else:
                match = self.DISPLAY_POSITION_REGEX.search(config_def['position'])
                if len(match.groups()) != 2:
                    raise Exception('Invalid display position definition: ' + config_def['position'])
                res.append('--{} {}'.format(match.group('location'), match.group('id')))
        if 'primary' in config_def and config_def['primary']:
            res.append('--primary')
        return ' '.join(res)

    def execute(self, configuration, system_state):
        """
        :type configuration: domain.Configuration
        :type system_state: domain.SystemState
        :return:
        """
        xrandr_conf = ''
        # We expect to get the list of devices
        for display_selector, config_def in self.definition.items():
            displays = system_state.default_screen.get_displays_by_wildcard(display_selector)
            for display in displays:
                xrandr_conf += self.create_xrandr_screen_for_display(display, config_def) + ' '
        print xrandr_conf

registry.register(ConfigureDisplaysExecutor)




