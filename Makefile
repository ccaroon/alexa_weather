ROOT=${PWD}

test: secrets clean
	# python -m unittest discover -v -s tests
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

package:
	cd venv/lib/python3.8/site-packages && zip -r9 /tmp/alexa_weather.zip . -x@${ROOT}/package-excludes.lst
	# cd venv/lib/python3.8/site-packages && zip -r9 /tmp/alexa_weather.zip .
	zip -g /tmp/alexa_weather.zip adafruit_io.py secrets.py weather.py
	mv /tmp/alexa_weather.zip .
	cp ./alexa_weather.zip ~/

# package: alexa_weather_package.zip

# alexa_weather_package.zip: secrets.py weather.py
# 	rm -f alexa_weather_package.zip
# 	mkdir package
# 	cp secrets.py weather.py package
# 	cp -a venv/lib/python2.7/site-packages/requests package
# 	cd package && zip -r ../alexa_weather_package.zip * && cd ..
# 	rm -rf package/

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
