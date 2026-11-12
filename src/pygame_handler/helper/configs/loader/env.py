from typing import cast

from pygame_handler.helper import debugger
from dotenv import load_dotenv as load_dotenv


from .shared import MISSING,expected_env_configs,env_FILE_NAME,truthy_values


def evaluate_boolean(string: str) -> bool:
    return string.lower() in truthy_values


from os import getenv as os_getenv
def get_env_value[T = str](
    option_name: str,
    default: str | T = "false",
) -> str | T:
    return os_getenv(option_name, default)


def load_configs():
    load_dotenv(env_FILE_NAME)

    print(f"Loading {len(expected_env_configs)} env configs...")

    option_ALL = get_env_value("ALL", MISSING)
    
    if option_ALL is not MISSING:
        all_configs_value = evaluate_boolean(option_ALL)

        

    show_updates = debugger.FLAGS.init_info

    for config_env_name , (config_location_ref, config_name) in expected_env_configs.items():
        if option_ALL is MISSING:
            option = get_env_value(config_env_name)
            value = evaluate_boolean(option)
        else:
            option = get_env_value(config_env_name, MISSING)
            if option is MISSING:
                value = all_configs_value
            else:
                value = evaluate_boolean(
                option)

        if value == getattr(config_location_ref, config_name):
            continue

        setattr(config_location_ref, config_name, value)

        if show_updates:
            config_location_ref = cast(str,config_location_ref.__name__)
            print("Config {}[{!r}] set to {!r}".format(config_location_ref, config_name, value))
    print(f"Updated configs.")
