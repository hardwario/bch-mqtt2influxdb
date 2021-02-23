#!/usr/bin/env python3

import os
import sys
import logging
import yaml
from schema import Schema, And, Or, Use, Optional, SchemaError
import jsonpath_ng
from .expr import parse_expression
import re

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
        return jsonpath_ng.parse(txt)
    except Exception as e:
        raise SchemaError('Bad JsonPath format: %s' % txt)


def str_or_jsonPath(txt):
    if "$." in txt:
        return json_path(txt)
    return txt


def str_or_jsonPath_or_expr(txt):
    if '=' in txt:
        return parse_expression(txt)
    return str_or_jsonPath(txt)


def valid_pycron_expr(txt):
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
        'host': And(str, len),
        'port': And(int, port_range),
        Optional('username'): And(str, len),
        Optional('password'): And(str, len),
        'database': And(str, len),
        Optional('ssl'): bool
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
        Optional('fields'): Or({str: Or(And(str, len, Use(str_or_jsonPath_or_expr)), {'value': And(str, len, Use(str_or_jsonPath_or_expr)), 'type': And(str, len)})}, And(str, len, Use(str_or_jsonPath_or_expr))),
        Optional('tags'): {str: And(str, len, Use(str_or_jsonPath))},
        Optional('database'): And(str, len)
    }]
})


def load_config(config_filename):
    with open(config_filename, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        try:
            return schema.validate(config)
        except SchemaError as e:
            # Better error format
            error = str(e).splitlines()
            del error[1]
            raise Exception(' '.join(error))
