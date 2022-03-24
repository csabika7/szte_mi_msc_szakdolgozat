from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='model-prediction-server',
    version='1.0.0',
    packages=[
        "model-prediction-server"
    ],
    zip_safe=False,
    install_requires=required
)

