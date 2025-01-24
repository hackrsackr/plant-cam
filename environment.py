#!/usr/bin/python3
import bme280
import smbus2

"""
The sample method will take a single reading and return a
compensated_reading object
    data = bme280.sample(bus, address, calibration_params)

The compensated_reading class has the following attributes
    attrs of data:
        data.id
        data.timestamp
        data.temperature
        data.pressure
        data.humidity
"""


def getBmeData(port: int = 1, addr: str = 0x76) -> object:
    """Returns entire data object from BME280"""
    bus: object = smbus2.SMBus(port)
    addr: str = addr
    params: object = bme280.load_calibration_params(bus, addr)
    data: object = bme280.sample(bus, addr, params)

    print(f"Data: {data}")

    return data


def getTempAndHumidity(port: int = 1, addr: str = 0x76) -> float:
    """Returns temp in F, and Humidity % from BME280"""
    bus: object = smbus2.SMBus(port)
    addr: str = addr
    params: object = bme280.load_calibration_params(bus, addr)
    data: object = bme280.sample(bus, addr, params)
    temperature: float = data.temperature * 9 / 5 + 32
    humidity: float = data.humidity

    return (temperature, humidity)


def main() -> None:
    temperature, humidity = getTempAndHumidity()

    print(f"Temperature: {temperature:.2f}\n" f"Humidity[%]: {humidity:.2f}")


if __name__ == "__main__":
    main()