import ast
import re
from setuptools import setup, find_packages

# retrieve __version__ number from __init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('cli.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

# retrieve long description from README.rst
with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name="jsoncat",
    version=version,
    url="http://github.com/json-transformations/jsoncat",
    keywords=['format', 'json', 'dump', 'console', 'terminal', 'command-line'],

    author="Brian Peterson",
    author_email="bpeterso2000@yahoo.com",

    description="Concatenate JSON FILE(s), or STDIN, format to STDOUT.",
    long_description=readme,

    packages=find_packages(include=['jsonls']),
    include_package_data=True,
    zipsafe=False,

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],

    install_requires=['click==6.7', 'contextlib2===0.5.5'],

    test_suite='tests',
    test_requires=['flake8', 'mock', 'pytest-cov', 'tox'],

    setup_requires=['pytest-runner'],

    entry_points={'console_scripts': ['jsoncat=cli:jsoncat']}
)
