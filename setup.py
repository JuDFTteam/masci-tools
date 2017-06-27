# -*- coding: utf-8 -*-
"""
setup: usage: pip install -e .[graphs]
"""

from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='plot_methods',
        version='0.1.0b',
        description='Wrapers of matplotlib functionality to visualalize common material science data. Plus wrapers of visualisation for aiida-fleur workflow nodes',
        url='https://bitbucket.org/broeder-j/plot_methods/',
        author='Jens Broeder',
        author_email='j.broeder@fz-juelich.de',
        license='MIT License, see LICENSE.txt file.',
        classifiers=[
            'Development Status :: 2 - Beta',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='material science plots fitting visualization aiida aiida-fleur flapw',
        packages=['src', 'tests'],
        include_package_data=True,
        
        install_requires=[
            'numpy',
            'matplotlib',
        ],
    )
