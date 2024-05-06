import os.path
import shutil

from invoke import task

import helper

BUILD_DETRITUS = [
    helper.PACKAGE["name"],
    helper.PACKAGE["dir"],
    "__pycache__/"
]

@task
def secrets(ctx):
    """ Create secrets.py """
    if not os.path.exists("secrets.py"):
        raise FileNotFoundError("Looks like you need to create the secrets.py file.")



@task(pre=[secrets])
def package(ctx):
    """ Create Code Package for Uploading to AWS """
    need_to_build = False

    if not os.path.exists(helper.PACKAGE["name"]):
        need_to_build = True
    else:
        for file in helper.PACKAGE["files"]:
            if helper.is_newer(file, helper.PACKAGE["name"]):
                need_to_build = True
                break

    if need_to_build:
        print("=> Removing Old Package...")
        if os.path.exists(helper.PACKAGE["name"]):
            os.unlink(helper.PACKAGE["name"])

        print("=> PIP Install...")
        ctx.run(f"pip install --target {helper.PACKAGE["dir"]} -r requirements.txt")
        
        print("=> Copy Src & Data Files...")
        ctx.run(f"cp {' '.join(helper.PACKAGE["files"])} {helper.PACKAGE["dir"]}")
        
        print("=> Zip Package Dir...")
        with ctx.cd(helper.PACKAGE["dir"]):
        	ctx.run(f"zip -r ../{helper.PACKAGE["name"]} *")
        
        print("=> Clean up...")
        shutil.rmtree(helper.PACKAGE["dir"])


@task
def clean(ctx):
    """ Cleanup Build Detritus """
    helper.clean(BUILD_DETRITUS)
