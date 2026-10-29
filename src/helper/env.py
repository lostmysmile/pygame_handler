from helper import debugger
from dotenv import load_dotenv as load_dotenv

from typing import Any

env_settings = {
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


def get_option[T = Any](optionname: str, default: T="false"):
    from os import getenv as os_getenv
    return os_getenv(optionname, default)


def load_debug_settings():
    changed_list = []

    print(f"Loading {len(env_settings)} env settings...")

    option_all = get_option("ALL", None)

    all_settings_value = evaluate_string_option(option_all)

    for (setting_location, setting_name), setting_env_name in env_settings.items():
        if option_all is not None:
            option = get_option(setting_env_name,None)
            new_value = evaluate_string_option(option) if option is not None else all_settings_value
        else:
            option = get_option(setting_env_name)
            new_value = evaluate_string_option(option)

        if new_value == getattr(setting_location, setting_name):
            continue
        
        changed_list.append((setting_location, setting_name, new_value))
        setattr(setting_location, setting_name, new_value)
    show_updates = debugger.FLAGS.init_info
    if show_updates:
        for setting_location, setting_name, new_value in changed_list:
            print(f"Setting {setting_location.__name__}[{setting_name!r}] set to {new_value!r}")
    print(f"Updated settings.")
