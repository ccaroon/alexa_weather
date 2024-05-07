# alexa_weather
An Alexa Skill to get Weather Data from My Local Weather Station

## Info
* [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/index.html)
* [ASK SDK for Python](https://developer.amazon.com/en-US/docs/alexa/alexa-skills-kit-sdk-for-python/overview.html)
* [ASK SDK Python API](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/api/core.html)

## Development Setup
1. Create a Python 3.12.x virtual environment
    - `python3.12 -mvenv venv`
    - OR
    - `pyenv virtualenv 3.12.2 alexa_weather`
2. Activate the Virtual Environment
    - `. venv/bin/active`
    - OR
    - `pyenv local alexa_weather`
3. Install dependencies
    * `pip install -r requirements-dev.txt`
4. Create a `secrets.py` file. See `secrets.py.dist`.
5. Test
    - `invoke check.coverage`
6. See `invoke -l`

## Packaging for AWS Lambda
[Detailed Information](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)

1. Build the package (zip file)
    - `inv build.package`
2. Upload to Lambda
    - `inv install.upload`
