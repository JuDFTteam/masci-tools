# -*- coding: utf-8 -*-
"""
setup: usage: pip install -e .[graphs]
"""

from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='masci_tools',
        version='0.2.0',
        description='Tools for Materials science. Vis contains wrapers of matplotlib functionality to visualalize common material science data. Plus wrapers of visualisation for aiida-fleur workflow nodes',
        url='https://github.com/JuDFTteam/masci-tools',
        author='Jens Broeder',
        author_email='j.broeder@fz-juelich.de',
        license='MIT License, see LICENSE.txt file.',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering :: Physics'
        ],
        keywords='material science plots fitting visualization aiida dft all-electron',
        packages=find_packages(),
        #['src', 'tests'],
        include_package_data=True,
        
        install_requires=[
            'numpy',
            'matplotlib',
        ],
    )
