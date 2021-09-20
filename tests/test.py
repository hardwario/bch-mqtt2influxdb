import unittest
import io
import sys
from paho.mqtt.client import MQTTMessage
from mqtt2influxdb.mqtt2influxdb import Mqtt2InfluxDB
from mqtt2influxdb.config import load_config


config = '''
mqtt:
  host: 127.0.0.1
  port: 1883

influxdb:
  host: 127.0.0.1
  port: 8086
  database: node

points:
  - measurement: temperature
    topic: node/+/thermometer/+/temperature
    fields:
      value: $.payload
    tags:
      id: $.topic[1]
      channel: $.topic[3]
'''


class fakeInfluxDBApi:
    def __init__(self):
        self.resetValues()

    def resetValues(self):
        self.data = []

    def write_points(self, points, database):
        self.data.append({
            'points': points,
            'database': 'node' if database is None else database
        })


class TestTransform(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestTransform, cls).setUpClass()
        cls.m2i = Mqtt2InfluxDB(load_config(io.StringIO(config)))
        cls.influxdb = fakeInfluxDBApi()
        cls.m2i._influxdb = cls.influxdb

        if sys.version_info[0] >= 3:
            # define some alias for python2 compatibility
            unicode = str

        def mqtt_pub(self, topic, payload):
            if isinstance(payload, unicode):
                local_payload = payload.encode('utf-8')
            elif isinstance(payload, (bytes, bytearray)):
                local_payload = payload
            elif isinstance(payload, (int, float)):
                local_payload = str(payload).encode('ascii')
            elif payload is None:
                local_payload = b''
            else:
                raise Exception('payload must be a string, bytearray, int, float or None.')
            message = MQTTMessage(0, topic.encode('utf-8'))
            message.payload = local_payload
            cls.m2i._on_mqtt_message(None, None, message)

        cls.mqtt_pub = mqtt_pub

    def setUp(self):
        self.influxdb.resetValues()

    def test_measurement_temperature(self):
        self.mqtt_pub('node/push-button:1/thermometer/0:1/temperature', 22.94)
        print(self.influxdb.data)
        self.assertEqual(len(self.influxdb.data), 1, msg='Expect 1 call write_points')
        self.assertEqual(len(self.influxdb.data[0]['points']), 1, msg='Expect 1 points')
        self.assertEqual(self.influxdb.data[0]['database'], 'node')
        point = self.influxdb.data[0]['points'][0]
        self.assertEqual(point['measurement'], 'temperature')
        self.assertEqual(point['fields']['value'], 22.94)
        self.assertDictEqual(point['tags'], {'id': 'push-button:1', 'channel': '0:1'})
        self.assertTrue('time' in point)


if __name__ == '__main__':
    unittest.main()
