import os
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setup(
    name='wallarm-fast-cli',
    version=version,
    description='A Wallarm FAST CLI tool for executing tests and getting results from the command line.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/faloker/wallarm-fast-cli',
    license='MIT',
    packages=[
        'fastcli',
    ],
    install_requires=[
        'click==7.0',
        'requests==2.23.0',
    ],
    entry_points={
        'console_scripts': [
            'fast-cli=fastcli.cli:cli',
        ],
    },
    classifiers=[
        'Topic :: Security',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
    ],
)
