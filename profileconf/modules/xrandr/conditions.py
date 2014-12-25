from profileconf.condition import Condition

__author__ = 'corvis'

MATCH_STRATEGY_EXACT = 'exact-match'
MATCH_STRATEGY_CONTAINS = 'contains'


class MonitorConnectedCondition(Condition):
    name = 'connected'
    aliases = ['connected-only']

    def __init__(self, ref_name, definition):
        self.strategy = MATCH_STRATEGY_CONTAINS
        self.display_id_list = []
        for x in definition.split(','):
            self.display_id_list.append(x.strip())
        if ref_name == 'connected-only':
            self.strategy = MATCH_STRATEGY_EXACT

    def evaluate(self, current_system_state):
        """
        :type current_system_state: domain.SystemState
        """
        screen = current_system_state.get_section('display').default_screen
        # Should be TRUE if all of the displays are connected
        for x in self.display_id_list:
            display_state = screen.get_display(x)
            if display_state is None or not display_state.is_connected:
                return False
        if self.strategy == MATCH_STRATEGY_EXACT:
            return len(self.display_id_list) == len(screen.get_connected_displays())
        return True
