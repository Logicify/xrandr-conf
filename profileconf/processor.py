import logging

__author__ = 'corvis'

__logger = logging.getLogger('processor')

ERROR_HANDLING_MODE_IGNORE = 0
ERROR_HANDLING_MODE_BREAK = 1
ERROR_HANDLING_MODE_EXCEPTION = 2


def find_matching_profiles(system_state, configuration):
    """
    Finds profiles which match current system state and returns the list as result
    :type system_state: domain.SystemState
    :type configuration: domain.Configuration
    :return: list of Profile objects
    """
    res = []
    # iterate over all profiles
    for profile_name, profile in configuration.profiles.items():
        # Skip profiles without conditions
        if len(profile.conditions) == 0:
            continue
        # Evaluate each condition and check if all of them returns TRUE on current system state
        positive_conditions_count = 0
        for condition in profile.conditions:
            if condition.evaluate(system_state):
                positive_conditions_count += 1
                __logger.debug('Condition {}: TRUE')

            else:
                __logger.debug('Condition {}: FALSE')
        # If all of conditions returned positive result - profile matches
        if len(profile.conditions) == positive_conditions_count:
            res.append(profile)
    return res


def activate_profile(profile, configuration, system_state, error_handling_mode=ERROR_HANDLING_MODE_IGNORE):
    """
    Invokes all executors for given profile
    :type profile: Executor
    :type system_state: domain.SystemState
    :type configuration: domain.Configuration
    """
    for executor in profile.executors:
        try:
            executor.execute(configuration, system_state)
        except Exception as e:
            __logger.exception("Executor failed: " + e.message, e)
            if error_handling_mode == ERROR_HANDLING_MODE_IGNORE:
                pass # Nothing to do here...
            elif error_handling_mode == ERROR_HANDLING_MODE_BREAK:
                return False
            elif error_handling_mode == ERROR_HANDLING_MODE_EXCEPTION:
                raise e
    return True