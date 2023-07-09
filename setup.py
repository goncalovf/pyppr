#!/usr/bin/env python

from os import path


def get_version():
    """
    Find the value assigned to __version__ in pyppr/__init__.py.

    This function assumes that there is a line of the form

        __version__ = "version-string"

    in that file.  It returns the string version-string, or None if such a
    line is not found.
    """
    with open("pyppr/__init__.py", "r") as f:
        for line in f:
            s = [w.strip() for w in line.split("=", 1)]
            if len(s) == 2 and s[0] == "__version__":
                return s[1][1:-1]


CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: Financial and Insurance Industry
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3 :: Only
Topic :: Software Development
Topic :: Office/Business :: Financial :: Investment
"""

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

if __name__ == "__main__":
    from setuptools import setup, find_packages

    setup(name='pyppr',
          version=get_version(),
          description='Financial functions regarding PPRs',
          long_description=long_description,
          long_description_content_type='text/markdown',
          packages=find_packages(exclude=['doc']),
          author='Gonçalo Vieira Figueiredo',
          license='BSD 3-Clause',
          maintainer='Gonçalo Vieira Figueiredo',
          maintainer_email='me@goncalovf.com',
          install_requires=[],
          python_requires='>=3.6',
          classifiers=CLASSIFIERS.splitlines(),
          url='',
          download_url='https://pypi.org/project/pyppr/',
          project_urls={})
