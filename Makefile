ROOT=${PWD}

test: secrets clean
	nosetests -v -s \
		--with-coverage \
		--cover-erase \
		--cover-html \
		--cover-inclusive \
		--cover-xml \
		--cover-package adafruit_io,secrets,weather

secrets: secrets.py

secrets.py:
	echo "Looks like you need to create the secrets.py file."
	exit 1

package: alexa_weather.zip

alexa_weather.zip: flask-ask *.py templates.yaml
	rm -f alexa_weather.zip
	pip install --target ./package -r requirements.txt
	cd flask-ask && pip install . --target ../package
	cp *.py templates.yaml package/
	cd package && zip -r ../alexa_weather.zip * && cd ..
	rm -rf package/

upload: alexa_weather.zip
	aws --profile the-weather-man lambda update-function-code --function-name TheWeatherMan --zip-file fileb://alexa_weather.zip

flask-ask:
	. venv/bin/activate
	git clone https://github.com/johnwheeler/flask-ask.git
	cp doc/flask-ask-reqs.txt flask-ask/requirements.txt
	cd flask-ask && python ./setup.py install

clean:
	rm -f alexa_weather.zip
	rm -f *.pyc
	rm -rf cover
	rm -f coverage.xml
	rm -rf flask-ask

.PHONY: test package clean
