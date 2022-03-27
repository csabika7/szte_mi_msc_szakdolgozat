from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='model-storage',
    version='1.0.0',
    packages=find_packages(),
    zip_safe=False,
    install_requires=required,
    testpaths='tests',
    source='model_storage'
)

