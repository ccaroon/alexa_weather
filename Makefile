test:
	python -m unittest discover -v -s tests

package:
	rm -f package.zip
	mkdir package
	cp weather.py package
	cp -a venv/lib/python2.7/site-packages/requests package
	cd package && zip -r ../package.zip * && cd ..
	rm -rf package/

clean:
	rm -rf package/
	rm -f package.zip
