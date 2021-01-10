# alexa_weather
An Alexa Skill to get the Weather from My Local Weather Station

## Info
* [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/index.html)

## Setup
1. Create a Python 3.8.x virtual environment
    - `python -mvenv venv`
2. Activate the Virtual Environment
    - `. venv/bin/active`
3. Install dependencies
    1. libs
        * YAML and YAML-Dev (May be needed by `PyYaml`)
            - Fedora/CentOS: `sudo yum install libyaml libyaml-devel`
            - Deb/Ubuntu: `sudo apt install libyaml-dev`
    2. pip
        * `pip install -r requirements-dev.txt`
        * Read [Flask-Ask](./doc/flask-ask.md) doc.
        * `make flask-ask`
4. Create a `secrets.py` file. See `secrets.py.dist`.
5. Test
    - `make test`

## Packaging for AWS Lambda
[Detailed Information](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)

1. Build the package (zip file)
    - `make package`
2. Upload to Lambda
    - `make upload`
