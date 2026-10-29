from pygame_handler.helper import debugger
from dotenv import load_dotenv as load_dotenv

from typing import Any

env_configs = {
    (debugger.FLAGS, "run_once"): "RUN_ONCE",
    (debugger.FLAGS, "debug_mode"): "DEBUG_MODE",
    (debugger.FLAGS, "detailed_info"): "DETAILED_INFO",
    (debugger.FLAGS, "init_info"): "INIT_INFO",
    (debugger.FLAGS, "event_info"): "EVENT_INFO",
    (debugger.FLAGS, "event_registers"): "EVENT_REGISTERS",
    (debugger.FLAGS, "states_info"): "STATES_INFO",
    (debugger.FLAGS, "state_context_info"): "STATE_CONTEXT_INFO",
    (debugger.FLAGS, "states_transitions"): "STATES_TRANSITIONS",
    (debugger.FLAGS, "time_internals"): "TIME_INTERNALS",
}

load_dotenv()


def evaluate_string_option(value: Any) -> bool:
    truthy_values = "1", "true", "on"
    return value in truthy_values


def get_option[T= Any](optionname: str, default: T="false"):
    from os import getenv as os_getenv
    return os_getenv(optionname, default)


def load_debug_configs():
    changed_list = []

    print(f"Loading {len(env_configs)} env configs...")

    option_all = get_option("ALL", None)

    all_configs_value = evaluate_string_option(option_all)

    for (config_location_name, config_name), config_env_name in env_configs.items():
        if option_all is not None:
            option = get_option(config_env_name, None)
            value = evaluate_string_option(
                option) if option is not None else all_configs_value
        else:
            option = get_option(config_env_name)
            value = evaluate_string_option(option)

        if value == getattr(config_location_name, config_name):
            continue

        changed_list.append((config_location_name.__name__, config_name, value))
        setattr(config_location_name, config_name, value)

    show_updates = debugger.FLAGS.init_info
    if show_updates:
        for details in changed_list:
            print("Config {}[{!r}] set to {!r}".format(*details))
    print(f"Updated configs.")
