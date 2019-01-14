#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine
"""Based on https://github.com/kennethreitz/setup.py"""

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command
from setuptools.command.test import test as TestCommand


# Package meta-data.
NAME = 'stranger'
DESCRIPTION = 'Annotate VCF files with str variants'
URL = 'https://github.com/moonso/stranger'
EMAIL = 'mans.magnusson@scilifelab.com'
AUTHOR = 'Måns Magnusson'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    'click',
    'coloredlogs',
    'pyyaml',
]

# What packages are optional?
EXTRAS = {
    'tests':['pytest','pytest-cov'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()

# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):

    """Set up the py.test test runner."""

    def finalize_options(self):
        """Set options for the command line."""
        TestCommand.finalize_options(self)
        self.test_args = ['--cov=stranger']
        self.test_suite = True

    def run_tests(self):
        """Execute the test runner command."""
        # Import here, because outside the required eggs aren't loaded yet
        import pytest
        sys.exit(pytest.main(self.test_args))

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),

    entry_points={
        'console_scripts': ["stranger = stranger.__main__:base_command"],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    tests_require=EXTRAS['tests'],
    include_package_data=True,
    license='MIT',
    keywords = ['vcf', 'variants', 'str'],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
        'test': PyTest,
    },
)
