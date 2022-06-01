ARG ARCH=
FROM ${ARCH}python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
CMD ["python3", "-m", "mqtt2influxdb.cli", "-c", "/config/config.yml"]
