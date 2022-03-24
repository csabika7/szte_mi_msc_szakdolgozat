from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='model-storage',
    version='1.0.0',
    packages=[
        "model-storage"
    ],
    zip_safe=False,
    install_requires=required
)

