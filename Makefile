.PHONY: clean

dev:
	pip install -e .

integration:
	python -m unittest discover -s tests/integration

dist: clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build \
		dist \
		cps_client.egg-info
