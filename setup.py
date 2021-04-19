# -*- coding: utf-8 -*-
"""
setup: usage: pip install -e .[graphs]
"""

from __future__ import absolute_import
from setuptools import setup, find_packages
import io  # needed to have `open` with encoding option

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf8') as f:
    long_description = f.read()

if __name__ == '__main__':
    setup(
        name='masci_tools',
        version='0.4.3',
        description='Tools for Materials science. Vis contains wrappers of matplotlib functionality to visualize common material science data. Plus wrappers of visualisation for aiida-fleur workflow nodes',
        # add long_description from readme.md:
        long_description = long_description, # add contents of README.md
        long_description_content_type ='text/markdown',  # This is important to activate markdown!
        url='https://github.com/JuDFTteam/masci-tools',
        author='Jens Broeder',
        author_email='j.broeder@fz-juelich.de',
        license='MIT License, see LICENSE.txt file.',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='material science plots fitting visualization aiida dft all-electron',
        packages=find_packages(),
        #['src', 'tests'],
        include_package_data=True,

        install_requires=[
            'numpy',
            'scipy',
            'matplotlib',
            'h5py',
            'pandas',
            'bump2version',
            'future',
            'lxml>=3.6.4',
            'more_itertools',
            'seaborn',
            'deepdiff',
            'humanfriendly',
            'mendeleev',
        ],
        extras_require={
            'pre-commit': [
                'pre-commit>=2.6.0',
                'yapf>=0.30.0',
                'pylint>=2.5.2',
                'pytest>=4.3.1'
            ],
            'docs': [
                'Sphinx',
                'docutils<0.17',
                'sphinx_rtd_theme'
            ],
            'testing': [
                'pytest>=4.3.1',
                'pytest-cov',
                'pytest-mpl',
                'pytest-regressions>=1.0'
            ],
            'bokeh-plots': [
                'bokeh<=1.4.0' # versions beyond 1.4.0 require a tornardo version not compatible with aiida-core /circus
            ]
        },
    )
