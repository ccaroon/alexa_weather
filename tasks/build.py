import os.path

from invoke import task

import utils

@task
def secrets(ctx):
    if not os.path.exists("secrets.py"):
        raise FileNotFoundError("Looks like you need to create the secrets.py file.")


# TODO: implement
# 	rm -f alexa_weather.zip
# 	pip install --target ./package -r requirements.txt
# 	cd flask-ask && pip install . --target ../package
# 	cp *.py templates.yaml package/
# 	cd package && zip -r ../alexa_weather.zip * && cd ..
# 	rm -rf package/
PACKAGE_FILES = [
    "adafruit_io.py",
    "weather.py",
    "templates.yaml"
]
PACKAGE_NAME = "alexa_weather.zip"
@task(pre=[secrets])
def package(ctx):
    need_to_build = False

    if not os.path.exists(PACKAGE_NAME):
        need_to_build = True
    else:
        for file in PACKAGE_FILES:
            if utils.is_newer(file, PACKAGE_NAME):
                need_to_build = True
                break

    if need_to_build:
        print("=> Building Package...")

@task
def clean(ctx):
    ctx.run("rm -f alexa_weather.zip")
    ctx.run("rm -rf __pycache__/")
    ctx.run("rm -rf cover/")
    ctx.run("rm -f coverage.xml")
