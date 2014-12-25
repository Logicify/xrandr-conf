import logging
import logging.config
import os

import yaml

from repository import ApplicationContext
import processor
import parser
from detector import Detector
from errors import InitializationError


__author__ = 'corvis'

if __name__ == '__main__':
    logging.config.dictConfig(yaml.load(file(os.path.join(os.path.dirname(__file__), 'logger.yaml'), 'r')))
    try:
        ApplicationContext().get().bootstrap()
    except InitializationError:
        exit(2)
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