import board
import adafruit_bme680

from flask import Flask, jsonify, request, redirect

from pathlib import Path

app = Flask(__name__)

sensor_name_file = Path("./sensor_name.txt")


def _get_sensor_name():
    return sensor_name_file.read_text().strip()


def _set_sensor_name(name):
    return sensor_name_file.write_text(name, encoding="utf-8")


def _get_temp_data():
    i2c = board.I2C()
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    return {
        "temperature_celsius": round(sensor.temperature, 2),
        "humidity": round(sensor.humidity, 2),
        "gas": sensor.gas,
        "sensor_name": _get_sensor_name(),
    }


@app.route("/api/data")
def sensor_data():
    return jsonify(_get_temp_data())


@app.route("/api/rename", methods=["POST"])
def set_sensor_name():
    _set_sensor_name(request.form.get("sensor_name"))
    return redirect("/")


@app.route("/rename")
def rename():
    return """
    <h1>Rename Sensor</h1>
    <form action="/api/rename" method="post">
        <label for="sensor_name">Sensor Name:</label><br>
        <input type="text" id="sensor_name" name="sensor_name"><br>
        <input type="submit" value="Submit">
    </form>
    """


@app.route("/data")
def data():
    data = _get_temp_data()
    return f"""
    <h1>Temperature Sensor: {data['sensor_name']}</h1>
    <p>Temperature: {data['temperature_celsius']}</p>
    <p>Humidity: {data['humidity']}</p>
    """


@app.route("/")
def home():
    return f"""
    <h1>Temperature Sensor: {_get_sensor_name()}</h1>
    <p><a href="/data">View Temperature/Humidity Data</a></p>
    <p><a href="/rename">Rename Sensor</a></p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0")
