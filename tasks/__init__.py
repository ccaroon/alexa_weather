from invoke import Collection, task

import build
import check
import install

@task(pre=[build.clean, check.clean])
def clean(ctx):
    """ Cleanup All the Things """
    pass

@task
def env(ctx):
    """
    Helps identify the python runtime environment
    """
    ctx.run("pyenv which python && python --version")


namespace = Collection(
    clean,
    build,
    check,
    install,
    env
)
