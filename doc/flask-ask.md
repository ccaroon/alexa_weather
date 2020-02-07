# Dealing with Flask-Ask

## Installation
As of Feb 6th, 2020.

### PIP
The version of Flask-Ask on PyPi  will NOT install
via `pip` versions >= 10.0. 

It claims to be v0.9.8.

### GitHub / Source
The version of the code in the `master` branch looks like it fixes the `pip` 
version >= 10 problem, but still fails to install under python 3.7 or 3.8. I didn't
test any other versions of python.

It claims to be v0.9.7 (As seen in the `setup.py` file).

### Work-A-Round
NOTE: The command `make flask-ask` will try to perform these steps for you.

I managed to get Flask-Ask to install by:

1. Checkout the code from GitHub: `git clone https://github.com/johnwheeler/flask-ask.git`
2. Update the `requirements.txt` file to look like this
```
    aniso8601==1.2.0
    Flask==1.1.1
    cryptography==2.8
    pyOpenSSL==19.1.0
    PyYAML==5.3
    six==1.14.0
```
3. `python ./setup.py install`
