import os
from invoke import task

import helper
import build


@task
def aws_cli(ctx):
    """ Install the AWS CLI v2 (iff not installed) """
    result = ctx.run("which aws", warn=True)
    if not result.stdout:
        print("=> Installing the AWS CLI...")
        with ctx.cd("/tmp"):
            ctx.run("curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip")
            ctx.run("unzip awscliv2.zip")
            ctx.run("sudo ./aws/install")
    else:
        print(f"=> The AWS Cli already exists at `{result.stdout.strip()}`")


@task(pre=[aws_cli, build.package])
def upload(ctx, profile="the-weather-man"):
    """ Upload the Zip Package to AWS Lambda """
    if not os.path.exists(".last-upload") or helper.is_newer(helper.PACKAGE['name'], ".last-upload"):
        ctx.run(f"aws --profile {profile} lambda update-function-code --function-name TheWeatherMan --zip-file fileb://{helper.PACKAGE['name']}")
        ctx.run("touch .last-upload")
    else:
        print(f"=> Nothing to do. {helper.PACKAGE['name']} has not changed since the last upload!")
