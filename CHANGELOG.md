# CHANGELOG

## 2024-05-07 - 2.0.0
* Updated to use Python 3.12 since Python 3.8 is deprecated on AWS
* Ditched `flask-ask` (way old and not working) for "AWS Ask SDK for Python"
* Ported `Makefile` to `invoke`.

## v1.1.0 - "v1.1.0" - [2021-01-10]
### Features
* [2021-01-10]
  * If the retrieved weather data is more than 5 minutes old, the Alexa response will say how old it is.
    - Example: "The temperature was 42 degrees 10 minutes ago."

## v1.0.0 - "ESPeranto" - [2020-02-07]
Complete re-write of the original code to use Flask-Ask and to pull data from
Adafruit IO.

## Legacy - "photon-particle-v1" - [2016-2017]
Original version of the code that uses "raw" python code and pulls data from
the Particle Cloud. This code now lives in the `photo-particle-v1` tag.
