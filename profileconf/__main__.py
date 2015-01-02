import os
import logging
import logging.config
from optparse import OptionParser
import time

import yaml
from profileconf import detector

import processor
import parser
from errors import InitializationError
from profileconf.repository import ApplicationContext


__author__ = 'corvis'

__time_tracking_logger = None
__application_logger = None


def get_config_path(arg_parser):
    fallback = [
        os.path.expanduser("~/.config/profile-conf/config.yaml"),
        os.path.expanduser("/etc/profile-conf/config.yaml"),
        os.path.join(os.path.dirname(__file__), 'config.yaml')
    ]
    config_path = (arg_parser.values.config_path if arg_parser.values.config_path is not None else None)
    if config_path is None:
        for x in fallback:
            if os.path.isfile(x):
                config_path = x
                break
    if config_path is None:
        raise Exception('Unable to find config file')
    __application_logger.debug('Using config file: ' + config_path)
    if not os.path.isfile(config_path):
        raise Exception("Config file {} doesn't exist".format(config_path))
    return file(config_path, 'r')


def initialize(arg_parser):
    """
    Bootstraps application and returns parsed config as result
    :return:
    """
    global __time_tracking_logger, __application_logger
    logging.config.dictConfig(yaml.load(file(os.path.join(os.path.dirname(__file__), 'logger.yaml'), 'r')))
    __time_tracking_logger = logging.getLogger('TimeTracking')
    __application_logger = logging.getLogger('Application')
    try:
        config_dict = parser.config_to_dict(get_config_path(arg_parser))
    except InitializationError as e:
        __application_logger.error("Config error: " + e.message)
        exit(3)
    try:
        start_time = time.time()
        ApplicationContext().get().bootstrap()
        initialization_time = time.time() - start_time
        __time_tracking_logger.info('Application bootstrap time: {}ms'.format(int(round(initialization_time*1000))))
    except InitializationError:
        exit(2)
    try:
         return parser.parse_config(config_dict)
    except InitializationError as e:
        print "Config error: " + e.message
        exit(2)


def command_list(option, opt, value, parser):
    pass
    exit()


def command_query(option, opt, value, parser):
    configuration = initialize(parser)
    # Capturing current system state
    system_state = detector.capture_system_state()
    print(system_state)
    exit()


def command_find_profiles(option, opt, value, parser):
    configuration = initialize(parser)
    # Capturing current system state
    system_state = detector.capture_system_state()
    # Find matching profiles
    matching_profiles = processor.find_matching_profiles(system_state, configuration)
    print(matching_profiles)
    exit()


arg_parser = OptionParser()
arg_parser.add_option("-c", "--config", type="string", dest="config_path",
                  help="""Sets path of the config file which should be used. If this option is not set application will try to find config in default locations:
<HOME_DIR>/.config/profile-conf/config.yaml, /etc/profile-conf/config.yaml
                """)
arg_parser.add_option("-l", "--list",
                  action="callback", callback=command_list,
                  help="List all available profiles.")
arg_parser.add_option("-q", "--query",
                  action="callback", callback=command_query,
                  help="Captures current system state and outputs result in readable form. "
                       "This can be very useful for debugging/composing config file")
arg_parser.add_option("-p", "--find-profiles",
                  action="callback", callback=command_find_profiles,
                  help="Detects which profiles could be applied")

if __name__ == '__main__':
    (options, args) = arg_parser.parse_args()
    configuration = initialize(arg_parser)
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