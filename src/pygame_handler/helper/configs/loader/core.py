from operator import attrgetter
from typing import Any

from pygame_handler.helper import debugger

MISSING = sentinel("MISSING")
ALL_CONFIGS_NAME = "all"

truthy_values = ("true",)

INI_FILE_NAME = "src/.ini"
env_FILE_NAME = "src/.env"

#? Structure=
#   option name: (variable location, variable name inside location)
expected_env_configs = {
    # "RUN_ONCE":(debugger.FLAGS, "run_once"),
    # "DEBUG_MODE":(debugger.FLAGS, "debug_mode"),
    # "DETAILED_INFO":(debugger.FLAGS, "detailed_info"),
    # "INIT_INFO":(debugger.FLAGS, "init_info"),
    # "EVENT_INFO":(debugger.FLAGS, "event_info"),
    # "EVENT_REGISTERS":(debugger.FLAGS, "event_registers"),
    # "STATES_INFO":(debugger.FLAGS, "states_info"),
    # "STATE_CONTEXT_INFO":(debugger.FLAGS, "state_context_info"),
    # "STATES_TRANSITIONS":(debugger.FLAGS, "states_transitions"),
    # "TIME_INTERNALS":(debugger.FLAGS, "time_internals"),
}

#? Structure= 
#   sections:
#       option name: (variable location, variable name inside location)

expected_ini_configs = {
    "INVALID":{},
    "LOOP": {
    "run_once":(debugger.FLAGS, "run_once"),
        },
    "DEBUGGER": {
    "debug_mode":(debugger.FLAGS, "debug_mode"),
    "detailed_info":(debugger.FLAGS, "detailed_info"),
    "init_info":(debugger.FLAGS, "init_info"),
    "config_info":(debugger.FLAGS, "config_info"),
    "event_info":(debugger.FLAGS, "event_info"),
    "event_registers":(debugger.FLAGS, "event_registers"),
    "states_info":(debugger.FLAGS, "states_info"),
    "state_context_info":(debugger.FLAGS, "state_context_info"),
    "states_transitions":(debugger.FLAGS, "states_transitions"),
    "time_internals":(debugger.FLAGS, "time_internals"),
    },
    
}

