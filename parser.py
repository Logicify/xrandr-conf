import yaml
from conditions import registry as conditions_registry
from executors import registry as executors_registry
from domain import Profile, Configuration

__author__ = 'corvis'


def parse_config(config_stream):
    config = yaml.load(config_stream)
    config_obj = Configuration()
    # Process "Profiles section"
    if 'profiles' not in config:
        raise Exception('\"profiles\" section is required')
    for profile_name, profileDef in config['profiles'].items():
        profile = Profile()
        profile.name = profile_name
        config_obj.profiles[profile_name] = profile
        # Is there any conditions?
        if 'when' in profileDef:
            # Iterate though conditions
            for condition_type, condition_def in profileDef['when'].items():
                condition = conditions_registry.create_condition(condition_type, condition_def)
                profile.conditions.append(condition)
        # Is there executors attached
        if 'then' in profileDef:
            for executor_wrapper in profileDef['then']:
                executor_type, executor_def = executor_wrapper.popitem()
                executor = executors_registry.create_executor(executor_type, executor_def)
                profile.executors.append(executor)
    return config_obj
