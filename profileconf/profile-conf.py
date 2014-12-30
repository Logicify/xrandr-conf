import logging
import logging.config
import os
import time

import yaml
from profileconf import detector

import processor
import parser
from errors import InitializationError
from profileconf.repository import ApplicationContext


__author__ = 'corvis'

if __name__ == '__main__':
    logging.config.dictConfig(yaml.load(file(os.path.join(os.path.dirname(__file__), 'logger.yaml'), 'r')))
    __time_tracking_logger = logging.getLogger('TimeTracking')
    __application_logger = logging.getLogger('Application')
    try:
        start_time = time.time()
        ApplicationContext().get().bootstrap()
        initialization_time = time.time() - start_time
        __time_tracking_logger.info('Application bootstrap time: {}ms'.format(int(round(initialization_time*1000))))
    except InitializationError:
        exit(2)
    try:
        configuration = parser.parse_config(file('./config.yaml', 'r'))
    except InitializationError as e:
        print "Config error: " + e.message
        exit(2)
    # Capturing current system state
    system_state = detector.capture_system_state()
    # Find matching profiles
    matching_profiles = processor.find_matching_profiles(system_state, configuration)
    if len(matching_profiles) > 0:
        profile = matching_profiles[0]
        __application_logger.info("Applying profile {}...".format(profile.verbose_name))
        res = processor.activate_profile(matching_profiles[0], configuration, system_state)
        if res:
            __application_logger.info("Profile {}:\tACTIVATED".format(profile.verbose_name))
        else:
            __application_logger.info("Profile {}:\tERROR".format(profile.verbose_name))