from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cps_client',
    version='0.1.8',
    packages=find_packages(),

    description='A Circle Platform Services Python Client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/belljustin/cps-client-python",
    author='J.D. Bell',
    author_email='justin.bell@mail.mcgill.ca',

    install_requires=[
        'click==7.1.1',
        'requests==2.23.0',
    ],
    entry_points={
        "console_scripts": [
            "cps = cps_client.cli:run"
        ]
    }
)
