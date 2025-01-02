import board
import adafruit_bme680

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api")
def sensor_data():
    i2c = board.I2C()
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    return jsonify({
        "temperature_celsius": sensor.temperature,
        "humidity": sensor.humidity,
        "gas": sensor.gas,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0")
