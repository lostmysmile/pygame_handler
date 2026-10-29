from helper import debug
from dotenv import load_dotenv as load_dotenv

from typing import Any

env_settings = {
    (debug.FLAGS, "run_once"): "RUN_ONCE",
    (debug.FLAGS, "debug_mode"): "DEBUG_MODE",
    (debug.FLAGS, "detailed_info"): "DETAILED_INFO",
    (debug.FLAGS, "event_info"): "EVENT_INFO",
    (debug.FLAGS, "event_registers"): "EVENT_REGISTERS",
    (debug.FLAGS, "states_info"): "STATES_INFO",
    (debug.FLAGS, "state_context_info"): "STATE_CONTEXT_INFO",
    (debug.FLAGS, "states_transitions"): "STATES_TRANSITIONS",
    (debug.FLAGS, "time_internals"): "TIME_INTERNALS",
}

load_dotenv()


def evaluate_string_option(value: str):
    truthy_values = "1", "true", "on"
    return value in truthy_values


def parse_option[T = Any](optionname: str, default: T="false"):
    from os import getenv as os_getenv
    return os_getenv(optionname, default)


def load_debug_settings():
    print(f"Loading {len(env_settings)} env settings...")
    changed_amount = 0
    option_all = parse_option("ALL", None)

    if option_all is None:
        all_settings_value = None
    else:
        all_settings_value = evaluate_string_option(option_all)

    for (setting_location, setting_name), setting_env_name in env_settings.items():
        if all_settings_value is not None:
            new_value = all_settings_value
        else:
            option = parse_option(setting_env_name)
            new_value = evaluate_string_option(option)

        if new_value == getattr(setting_location, setting_name):
            continue
        changed_amount += 1
        print(f"{setting_location.__name__}[{setting_name!r}] set to {new_value!r}")
        setattr(setting_location, setting_name, new_value)
    print(f"Updated {changed_amount} settings.")
