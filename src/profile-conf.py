import logging
import logging.config
import os

import yaml


__author__ = 'corvis'

if __name__ == '__main__':
    logging.config.dictConfig(yaml.load(file(os.path.join(os.path.dirname(__file__), 'logger.yaml'), 'r')))
    from src import conditions, processor, executors, parser
    from src.detector import Detector
    from src.errors import InitializationError
    try:
        conditions.registry.autodiscover()
        executors.registry.autodiscover()
    except InitializationError as e:
        print "Initialization error:" + e.message
        exit(1)
    try:
        configuration = parser.parse_config(file('./config.yaml', 'r'))
    except InitializationError as e:
        print "Config error: " + e.message
        exit(2)
    # Capturing current system state
    detector = Detector()
    system_state = detector.capture_system_state()
    # Find matching profiles
    matching_profiles = processor.find_matching_profiles(system_state, configuration)
    if len(matching_profiles) > 0:
        profile = matching_profiles[0]
        print "Applying profile {}...".format(profile.name)
        res = processor.activate_profile(matching_profiles[0], configuration, system_state)
        if res:
            print "Profile {}:\tACTIVATED".format(profile.name)
        else:
            print "Profile {}:\tERROR".format(profile.name)