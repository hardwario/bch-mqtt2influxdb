#!/usr/bin/env python3

import os
import sys
import logging
import yaml
from schema import Schema, And, Or, Use, Optional, SchemaError
import jsonpath_ng


def json_path(txt):
    try:
        return jsonpath_ng.parse(txt)
    except Exception as e:
        raise SchemaError('Bad JsonPath format: %s' % txt)


def str_or_jsonPath(txt):
    if "$." in txt:
        return json_path(txt)
    return txt


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
    'influxdb': {
        'host': And(str, len),
        'port': And(int, port_range),
        Optional('username'): And(str, len),
        Optional('password'): And(str, len),
        'database': And(str, len),
        Optional('ssl'): bool
    },
    'points': [{
        'measurement': And(str, len, Use(str_or_jsonPath)),
        'topic': And(str, len),
        Optional('fields'): Or({str: And(str, len, Use(str_or_jsonPath))}, And(str, len, Use(str_or_jsonPath))),
        Optional('tags'): {str: And(str, len, Use(str_or_jsonPath))},
        Optional('database'): And(str, len)
    }]
})


def load_config(config_filename):
    with open(config_filename, 'r') as f:
        config = yaml.load(f)
        try:
            return schema.validate(config)
        except SchemaError as e:
            # Better error format
            error = str(e).splitlines()
            del error[1]
            raise Exception(' '.join(error))
