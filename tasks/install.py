from invoke import task

import build


@task
def aws_cli(ctx):
    result = ctx.run("which aws", warn=True)
    if not result.stdout:
        with ctx.cd("/tmp"):
            ctx.run("curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip")
            ctx.run("unzip awscliv2.zip")
            ctx.run("sudo ./aws/install")


@task(pre=[aws_cli, build.package])
def upload(ctx):
    ctx.run("aws --profile the-weather-man lambda update-function-code --function-name TheWeatherMan --zip-file fileb://alexa_weather.zip")
