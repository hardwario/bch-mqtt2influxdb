<a href="https://www.hardwario.com/"><img src="https://www.hardwario.com/ci/assets/hw-logo.svg" width="200" alt="HARDWARIO Logo" align="right"></a>

# MQTT to InfluxDB

[![Travis](https://img.shields.io/travis/hardwario/bch-mqtt2influxdb/master.svg)](https://travis-ci.org/hardwario/bch-mqtt2influxdb)
[![Release](https://img.shields.io/github/release/hardwario/bch-mqtt2influxdb.svg)](https://github.com/hardwario/bch-mqtt2influxdb/releases)
[![PyPI](https://img.shields.io/pypi/v/mqtt2influxdb.svg)](https://pypi.org/project/mqtt2influxdb/)
[![License](https://img.shields.io/github/license/hardwario/bch-mqtt2influxdb.svg)](https://github.com/hardwario/bch-mqtt2influxdb/blob/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/follow/hardwario_en.svg?style=social&label=Follow)](https://twitter.com/hardwario_en)


## Example

```
mqtt2influxdb -c /etc/hardwario/mqtt2influxdb.yaml --debug
```

## How to install & configure

https://tower.hardwario.com/en/latest/tutorials/mqtt-to-influxdb/

## Local development

for Linux
```
git clone git@github.com:hardwario/bch-mqtt2influxdb.git
cd bch-mqtt2influxdb
./test.sh
. .venv/bin/activate
python3 setup.py develop
mqtt2influxdb -h
```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT/) - see the [LICENSE](LICENSE) file for details.

---

Made with &#x2764;&nbsp; by [**HARDWARIO s.r.o.**](https://www.hardwario.com/) in the heart of Europe.
