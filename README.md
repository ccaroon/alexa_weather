# alexa_weather
An Alexa Skill to get the Weather from My Local Weather Station

## Setup
1. Create a Python 3.8.x virtual environment
    - `python -mvenv venv`
2. Activate the Virtual Environment
    - `. venv/bin/active`
3. Install dependencies
   1. libs
      * YAML and YAML-Dev
        - Fedora/CentOS: `sudo yum install libyaml libyaml-devel`
        - Deb/Ubuntu: `sudo apt install libyaml-dev`
   2. pip
    - `pip install -r requirements-dev.txt`
    - Read [Flask-Ask](./doc/flask-ask.md) doc.
    - `make flask-ask`
4. Create a `secrets.py` file. See `secrets.py.dist`.
5. Test
    - `make test`

## Packaging for AWS Lambda
1. Build the package (zip file)
    - `make package`
2. Upload to Lambda via AWS Console
