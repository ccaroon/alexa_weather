import os
import shutil

PACKAGE = {
    "name": "alexa_weather.zip",
    "files": [
        "adafruit_io.py",
        "secrets.py",
        "version.py",
        "weather_station.py"
    ],
    "dir": "./package/"
}


def clean(files):
    for item in files:
        if os.path.isfile(item):
            print(f"=> Removing File: {item}...")
            os.unlink(item)
        elif os.path.isdir(item):
            print(f"=> Removing Dir: {item}...")
            shutil.rmtree(item)


def is_newer(file1, file2):
    """
    Is `file1` newer than `file2`?

    Args:
        file1 (str): Path to a file
        file2 (str): Path to a file
    """
    mt1 = os.path.getmtime(file1)
    mt2 = os.path.getmtime(file2)

    return mt1 > mt2
