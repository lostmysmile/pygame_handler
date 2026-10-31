import configparser
from pygame_handler.helper import debugger

from typing import Any

expected_ini_configs = {
    "run_once":(debugger.FLAGS, "run_once"),
    "debug_mode":(debugger.FLAGS, "debug_mode"),
    "detailed_info":(debugger.FLAGS, "detailed_info"),
    "init_info":(debugger.FLAGS, "init_info"),
    "event_info":(debugger.FLAGS, "event_info"),
    "event_registers":(debugger.FLAGS, "event_registers"),
    "states_info":(debugger.FLAGS, "states_info"),
    "state_context_info":(debugger.FLAGS, "state_context_info"),
    "states_transitions":(debugger.FLAGS, "states_transitions"),
    "time_internals":(debugger.FLAGS, "time_internals"),
}

def config_parser_parse(configs: configparser.SectionProxy,config_name):
    config_value = configs.get(config_name)
    try:
        config_value = configs.getboolean(config_name)
    except ValueError:
        pass
    try:
        config_value = configs.getfloat(config_name)
    except ValueError:
        pass
    try:
        config_value = configs.getint(config_name)
    except ValueError:
        pass
    return config_value


def evaluate_string_option(value: str) -> bool:
    truthy_values = "1", "true", "on"
    return value.lower() in truthy_values

MISSING = sentinel("MISSING")
FILE_NAME = "src/.ini"

def load_debug_configs():
    configs = configparser.ConfigParser()
    configs.read(FILE_NAME)
    print(f"Loaded {(configs.sections())} from .ini configs...")

    try:
        debug_configs = configs["DEBUGGER"]
    except KeyError:
        raise LookupError("Could not find 'DEBUGGER' in .ini")
        
    

    ALL_CONFIGS_NAME = "all"
    all_configs_value = debug_configs.getboolean(ALL_CONFIGS_NAME,MISSING)

    show_updates = __debug__ or debugger.FLAGS.init_info

    if (all_configs_value) is not MISSING:
        if show_updates:
            print("Setting all to",repr(str(all_configs_value)))

        for config_name,(config_location_name, config_name) in expected_ini_configs.items():
            setattr(config_location_name, config_name, all_configs_value)
    for config_name in debug_configs:
        try:
            (config_location_name, config_name) = expected_ini_configs[config_name]
        except KeyError:
            print("skipped",config_name)
            continue 
        config_value = config_parser_parse(debug_configs,config_name)
        print(config_value)
        
        if config_value == getattr(config_location_name, config_name):
            continue

        setattr(config_location_name, config_name, config_value)

        if show_updates:
            print("Config {}[{!r}] set to {!r}".format(expected_ini_configs.get(config_name,""),config_name,config_value))

    print(f"Updated configs.")
