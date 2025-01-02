import board
import adafruit_bme680

from flask import Flask, jsonify

app = Flask(__name__)


def _get_temp_data():
    i2c = board.I2C()
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    return {
        "temperature_celsius": round(sensor.temperature, 2),
        "humidity": round(sensor.humidity, 2),
        "gas": sensor.gas,
    }


@app.route("/api")
def sensor_data():
    return jsonify(_get_temp_data())


@app.route("/")
def home():
    data = _get_temp_data()
    return f"""
    <h1>Temperature Sensor</h1>
    <p>Temperature: {data['temperature_celsius']}</p>
    <p>Humidity: {data['humidity']}</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0")
