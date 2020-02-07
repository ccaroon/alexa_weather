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

alexa_weather.zip: *.py package-excludes.lst templates.yaml
	cd venv/lib/python3.8/site-packages && zip -r9 /tmp/alexa_weather.zip . -x@${ROOT}/package-excludes.lst
	zip -g /tmp/alexa_weather.zip *.py templates.yaml
	mv /tmp/alexa_weather.zip .
	cp ./alexa_weather.zip ~/

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
