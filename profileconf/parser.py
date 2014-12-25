from collections import OrderedDict

import yaml

from domain import Profile, Configuration
from repository import ApplicationContext

__author__ = 'corvis'


def yaml_load_ordered_dict_support(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def yaml_dump_ordered_dict_support(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


def parse_config(config_stream):
    config = yaml_load_ordered_dict_support(config_stream)
    config_obj = Configuration()
    # Process "Profiles section"
    if 'profiles' not in config:
        raise Exception('\"profiles\" section is required')
    conditions_registry = ApplicationContext.get().conditions_repository
    executors_registry = ApplicationContext.get().executors_repository
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
