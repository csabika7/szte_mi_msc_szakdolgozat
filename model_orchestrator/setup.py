from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='model-orchestrator',
    version='1.0.0',
    packages=find_packages(),
    package_data={'': ['*.yaml']},
    zip_safe=False,
    install_requires=required
)

