"""
setup: usage: pip install -e .[graphs]
"""

from setuptools import setup, find_packages
import io  # needed to have `open` with encoding option

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf8') as f:
    long_description = f.read()

if __name__ == '__main__':
    setup(
        name='masci_tools',
        version='0.7.2',
        description=
        'Tools for Materials science. Vis contains wrappers of matplotlib functionality to visualize common material science data. Plus wrappers of visualisation for aiida-fleur workflow nodes',
        # add long_description from readme.md:
        long_description=long_description,  # add contents of README.md
        long_description_content_type='text/markdown',  # This is important to activate markdown!
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
            'Programming Language :: Python :: 3.10',
            'Topic :: Scientific/Engineering :: Physics',
        ],
        keywords='material science plots fitting visualization aiida dft all-electron',
        packages=find_packages(exclude=['tests*']),
        #['src', 'tests'],
        include_package_data=True,
        install_requires=[
            'numpy', 'scipy', 'matplotlib', 'h5py', 'pandas', 'ase', 'bump2version', 'future', 'lxml>=4.5',
            'more_itertools', 'seaborn', 'deepdiff', 'humanfriendly', 'mendeleev', 'click', 'click-completion',
            'PyYAML', 'typing-extensions', 'tabulate'
        ],
        extras_require={
            'pre-commit':
            ['mypy==0.930', 'pre-commit>=2.6.0', 'yapf>=0.30.0', 'pylint~=2.11.1', 'pytest~=6.0', 'lxml-stubs'],
            'docs': [
                'Sphinx', 'docutils', 'sphinx_rtd_theme', 'sphinx-click', 'sphinx-toolbox<=2.15.2',
                'sphinx-autodoc-typehints'
            ],
            'testing': ['pytest~=6.0', 'pytest-cov', 'pytest-mpl>=0.12', 'pytest-regressions>=1.0'],
            'bokeh-plots': [
                'bokeh<=1.4.0'  # versions beyond 1.4.0 require a tornardo version not compatible with aiida-core /circus
            ],
            'cmdline-extras': ['python-gitlab']
        },
        entry_points={'console_scripts': [
            'masci-tools = masci_tools.cmdline.commands.root:cli',
        ]})
