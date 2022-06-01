import os
import sys
import logging
import yaml
import re
import jsonpath_ng
from io import IOBase
from schema import Schema, And, Or, Use, Optional, SchemaError
from .expr import parse_expression


class ConfigError(Exception):
    pass


# Regex for schedule config entries
validate_crontab_time_format_regex = re.compile(
    r"{0}\s+{1}\s+{2}\s+{3}\s+{4}".format(
        r"(?P<minute>\*|[0-5]?\d)",
        r"(?P<hour>\*|[01]?\d|2[0-3])",
        r"(?P<day>\*|0?[1-9]|[12]\d|3[01])",
        r"(?P<month>\*|0?[1-9]|1[012])",
        r"(?P<day_of_week>\*|[0-6](\-[0-6])?)"
    )  # end of str.format()
)  # end of re.compile()


def json_path(txt):
    try:
        logging.debug("validating as json path - '%s'" % txt)
        return jsonpath_ng.parse(txt)
    except Exception as e:
        logging.error("Bad JsonPath format: '%s'" % txt)
        raise SchemaError(['Bad JsonPath format: %s' % txt], str(e))


def str_or_jsonPath(txt):
    if "$." in txt:
        return json_path(txt)
    logging.debug("validating as string - '%s'" % txt)
    return txt


def str_or_jsonPath_or_expr(txt):
    if '=' in txt:
        logging.debug("validating as expression - '%s'" % txt)
        return parse_expression(txt)
    return str_or_jsonPath(txt)


def valid_pycron_expr(txt):
    logging.debug("validating as crontab entry - '%s'" % txt)
    if validate_crontab_time_format_regex.match(txt):
        return True
    raise SchemaError('Bad crontab format: %s' % txt)


def port_range(port):
    return 0 <= port <= 65535


schema = Schema({
    'mqtt': {
        'host': And(str, len),
        'port': And(int, port_range),
        Optional('username'): And(str, len),
        Optional('password'): And(str, len),
        Optional('cafile'): os.path.exists,
        Optional('certfile'): os.path.exists,
        Optional('keyfile'): os.path.exists,
    },
    Optional('http'): {
        'destination': And(str, len),
        'action': And(str, len),
        Optional('username'): And(str, len),
        Optional('password'): And(str, len)
    },

    'influxdb': {
        'url': And(str, len),
        'bucket': And(str, len),
        Optional('org'): str,
        Optional('token'): str,
    },
    Optional("base64decode"): {
        'source': And(str, len, Use(str_or_jsonPath)),
        'target': And(str, len)
    },
    'points': [{
        'measurement': And(str, len, Use(str_or_jsonPath)),
        'topic': And(str, len),
        Optional('schedule'): And(str, len, valid_pycron_expr),
        Optional('httpcontent'): {str: And(str, len, Use(str_or_jsonPath))},
        Optional('fields'): Or(
            {str: Or(And(str, len, Use(str_or_jsonPath_or_expr)),
                     {'value': And(str, len, Use(str_or_jsonPath_or_expr)), 'type': And(str, len)})},
            And(str, len, Use(str_or_jsonPath_or_expr))
        ),
        Optional('tags'): {str: And(str, len, Use(str_or_jsonPath))},
        Optional('database'): And(str, len)
    }]
})


def load_config(config_file):
    if isinstance(config_file, IOBase):
        config = yaml.safe_load(config_file)
        try:
            config = schema.validate(config)
        except SchemaError as e:
            raise ConfigError(str(e))
    elif config_file is None:
        config = {}
    else:
        raise ConfigError('Unknown type config_file')

    return config
