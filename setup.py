import re
import ast
from setuptools import setup

requirements = ['click>=6.7']
test_requirements = ['flake8', 'pytest-cov']

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('jsoncat/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='json-cat',
    version=version,
    author='Brian Peterson',
    author_email='bpeterso2000@yahoo.com',
    url='http://github.com/bpeterso2000/jsoncat',
    packages=['jsoncat'],
    description='Concatenate JSON FILE(s), or STDIN, format to STDOUT.',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3'],
    install_requires=requirements,
    tests_require=test_requirements,
    entry_points={'console_scripts': ['jsncat=jsoncat.cli:main']}
)
