import re
from profileconf.executor import Executor
from profileconf.modules.xrandr import context
from tools import run_xrandr_command

__author__ = 'corvis'


class XrandrExecutor(Executor):
    name = "xrandr"

    def __init__(self, ref_name, definition):
        super(XrandrExecutor, self).__init__()
        self.cmd_options = definition

    def execute(self, configuration, system_state):
        super(XrandrExecutor, self).execute(configuration, system_state)
        #run_xrandr_command(self.cmd_options)


class ConfigureDisplaysExecutor(Executor):
    """
    Provides following context variables:
    Expected config:
        <device wildcard>:
            <device configuration options> - see create_xrandr_screen_for_display docs for details
    On display section level:
        * $preferredResolution - preferred resolution of the gi
    """
    name = "configure-displays"
    COORDS_REGEX = re.compile('^\d+x\d+$')
    DISPLAY_POSITION_REGEX = re.compile('(?P<location>left\-of|right\-of|below|above)\s+(?P<id>[\w\d]+)')

    def __init__(self, ref_name, definition):
        super(ConfigureDisplaysExecutor, self).__init__()
        self.definition = definition

    def create_xrandr_screen_for_display(self, display, config_def):
        """
        See example definition for reference:
            state: "on"|"off"
            primary: true|false
            mode: "1920x1080"
            position: "0x0" | left-of <ID> | right-of <ID> | below <ID> | above <ID>
            rotate: "normal"
            auto: true
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
        if 'auto' in config_def and config_def['auto']:
            res.append('--auto')
        return ' '.join(res)

    def initialize_context(self, configuration, system_state):
        # this one expects to have "current_display" in context
        self.register_context_function(context.predefined_resolution)

    def execute(self, configuration, system_state):
        """
        :type configuration: domain.Configuration
        :type system_state: domain.SystemState
        :return:
        """
        super(ConfigureDisplaysExecutor, self).execute(configuration, system_state)
        display_system_state = system_state.get_section('display')
        xrandr_conf = ''
        # We expect to get the list of devices
        for display_selector, config_def in self.definition.items():
            displays = display_system_state.default_screen.get_displays_by_wildcard(display_selector)
            for display in displays:
                local_context = {
                    "current_display": display
                }
                xrandr_conf += self.create_xrandr_screen_for_display(display,
                                                                     self.preprocess_user_object(config_def,
                                                                                                 local_context)) + ' '
        print xrandr_conf
        #run_xrandr_command(xrandr_conf)