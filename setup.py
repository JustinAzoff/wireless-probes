from setuptools import setup, find_packages
from glob import glob

setup(name="wirelessprobe",
    version="1.0",
    author="Justin Azoff",
    author_email="JAzoff@uamail.albany.edu",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    entry_points = {
        'console_scripts': [
        "wireless-check = wirelessprobe.check:main"
        ]
    },
    scripts=glob('scripts/*'),
    #setup_requires=[
    #    "nose",
    #],
    test_suite='nose.collector',
)
