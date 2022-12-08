from setuptools import setup

long_description = None

with open("README.md", 'r') as fp:
    long_description = fp.read()

setup(
    name = "pySanutalAir",
    packages = ["sanutal_air"],
    version="0.1.6",
    description="Python3 library for home ventilation system from Sanutal",
    long_description=long_description,
    python_requires='>=3.6.7',
    author="Guillaume-HIS",
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
)
