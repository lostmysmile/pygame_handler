def load_settings():
    from dotenv import load_dotenv as load_dotenv
    load_dotenv()

    from helper import debug
    from os import getenv as os_getenv
    
    if not debug.run_once:
        debug.run_once = os_getenv("RUN_LOOP_ONCE", None) is not None
