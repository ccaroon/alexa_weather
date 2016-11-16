test:
	./src/weather.py

package:
	rm -f package.zip
	mkdir package
	cp src/*.py package
	cp -a venv/lib/python2.7/site-packages/* package
	cd package && zip -r ../package.zip * && cd ..
	rm -rf package/

clean:
	rm -rf package/
	rm -f package.zip
