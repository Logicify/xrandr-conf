from profileconf.condition import Condition
from profileconf.domain import RestrictedList

__author__ = 'corvis'


class MonitorConnectedCondition(Condition):
    name = 'connected'

    def __init__(self):
        super(MonitorConnectedCondition, self).__init__()
        self.display_id_list = RestrictedList()

    def initialize(self, ref_name, definition):
        if isinstance(definition, basestring):
            for x in definition.split(','):
                self.display_id_list.append(x.strip())
        elif isinstance(definition, RestrictedList):
            self.display_id_list = definition

    def evaluate(self, current_system_state):
        """
        :type current_system_state: domain.SystemState
        """
        screen = current_system_state.get_section('display').default_screen
        connected_display_names = [x.id for x in screen.get_connected_displays()]
        return self.display_id_list.match(connected_display_names)
