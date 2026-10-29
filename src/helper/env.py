from helper import debug
from dotenv import load_dotenv as load_dotenv


def evaluate_option(value: str):
    truthy_values = "1", "true", "on"
    return value in truthy_values


def parse_option(optionname: str, default="false"):
    from os import getenv as os_getenv
    return os_getenv(optionname, default).lower()


settings = {"run_once": "RUN_LOOP_ONCE"}

load_dotenv()


def load_debug_settings():

    for setting_name in debug.env_settings:
        option = parse_option("RUN_LOOP_ONCE")
        new_value = evaluate_option(option)
        if debug.FLAGS.debug_mode:
            print(f"Setting {setting_name!r} set to {new_value!r}")
        setattr(debug, setting_name, new_value)
