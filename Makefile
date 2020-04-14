.PHONY: clean

dist: clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build \
		dist \
		cps_client.egg-info
