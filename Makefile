test: secrets clean
	python -m unittest discover -v -s tests

secrets: secrets.py
	
secrets.py:
	echo "Looks like you need to create the secrets.py file."
	exit 1
	
package: package.zip

package.zip: secrets.py weather.py
	rm -f package.zip
	mkdir package
	cp secrets.py weather.py package
	cp -a venv/lib/python2.7/site-packages/requests package
	cd package && zip -r ../package.zip * && cd ..
	rm -rf package/

clean:
	rm -rf package/
	rm -f package.zip
	rm -f *.pyc
