from invoke import Collection, task

import build
import check
import install

@task
def env(ctx):
    """
    Helps identify the python runtime environment
    """
    ctx.run("pyenv which python && python --version")


namespace = Collection(
    build,
    check,
    install,
    env
)
