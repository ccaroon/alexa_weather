from invoke import task

import helper
import build


@task
def aws_cli(ctx):
    """ Install the AWS CLI v2 (iff not installed) """
    result = ctx.run("which aws", warn=True)
    if not result.stdout:
        with ctx.cd("/tmp"):
            ctx.run("curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip")
            ctx.run("unzip awscliv2.zip")
            ctx.run("sudo ./aws/install")


@task(pre=[aws_cli, build.package])
def upload(ctx, profile="the-weather-man"):
    """ Upload the Zip Package to AWS Lambda """
    ctx.run(f"aws --profile {profile} lambda update-function-code --function-name TheWeatherMan --zip-file fileb://{helper.PACKAGE['name']}")
