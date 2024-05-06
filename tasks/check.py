from invoke import task

import build
import helper

CHECK_DETRITUS = [
    "__pycache__/",
    "htmlcov/",
    ".coverage",
    "coverage.xml"
]

FILES = [
    "adafruit_io.py",
    "secrets.py",
    "weather_report.py"
]
@task(pre=[build.secrets])
def coverage(ctx):
    """ Run Code Coverage """
    ctx.run("coverage run -m nose2 -v tests")
    ctx.run(f"coverage report -m --fail-under=95 --include={','.join(FILES)}")
    ctx.run(f"coverage html --include={','.join(FILES)}")
    ctx.run(f"coverage xml --include={','.join(FILES)}")


@task
def clean(ctx):
    """ Cleanup Check Detritus """
    helper.clean(CHECK_DETRITUS)
