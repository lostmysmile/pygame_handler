import configparser
from pygame_handler.helper import debugger
from pygame_handler.helper.attributes import attrsetter

from .shared import (
    MISSING,
    ALL_CONFIGS_NAME,
    truthy_values, # pyright: ignore[reportUnusedImport]
    expected_ini_configs,
    INI_FILE_NAME,
)  


def config_parser_parse(configs: configparser.SectionProxy, config_name: str):
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


def load_configs():
    config_parser = configparser.ConfigParser()
    config_parser.read(INI_FILE_NAME)

    print(f"Found {(config_parser.sections())} sections in {INI_FILE_NAME!r}...")

    for section_name in expected_ini_configs:
        print(f"Loading section: {section_name!r}")
        try:
            section = config_parser[section_name]
        except KeyError:
            if debugger.FLAGS.config_info:
                print(f"section {section_name!r} not in {INI_FILE_NAME!r}")
            continue

        _load_section(section, section_name)


def _load_section(configs: configparser.SectionProxy, section_name: str):
    all_configs_value = configs.getboolean(ALL_CONFIGS_NAME, MISSING)

    show_updates = debugger.FLAGS.config_info

    if (all_configs_value) is not MISSING:
        if show_updates:
            print("All settings set to", repr(str(all_configs_value)))

        for config_name, (config_location_name, config_name) in expected_ini_configs[
            section_name
        ].items():
            attrsetter(config_location_name, config_name, all_configs_value)

    for config_name in configs:
        if config_name == ALL_CONFIGS_NAME:
            continue

        try:
            config_location_name, config_name = expected_ini_configs.get(
                section_name, {}
            )[config_name]
        except KeyError:
            print(
                "config name not found:",
                repr(config_name),
            )
            continue

        config_value = config_parser_parse(configs, config_name)

        if config_value == getattr(config_location_name, config_name):
            continue

        attrsetter(config_location_name, config_name, config_value)

        if show_updates:
            print(
                "Config {}[{!r}] set to {!r}".format(
                    expected_ini_configs.get(config_name, ""), config_name, config_value
                )
            )

    print(f"Finished section: {section_name!r}")
