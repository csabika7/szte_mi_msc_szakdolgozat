from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='model-prediction-aggregator',
    version='1.0.0',
    packages=find_packages(),
    zip_safe=False,
    install_requires=required
)

