from invoke import task

import build

@task(pre=[build.secrets])
def coverage(ctx):
    """ Run Code Coverage """
    ctx.run("coverage run -m nose2 -v tests")
    ctx.run("coverage report -m --fail-under=95 --include=adafruit_io,secrets,weather")
    ctx.run("coverage html --include=adafruit_io,secrets,weather")
    ctx.run("coverage xml --include=adafruit_io,secrets,weather")
