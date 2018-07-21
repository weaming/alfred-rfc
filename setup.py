# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

gh_repo = 'https://github.com/weaming/alfred-rfc'

setup(
    name='alfred-rfc',  # Required

    version='0.2.1',  # Required

    # This is a one-line description or tagline of what your project does.
    description='Search RFCs using alfred',  # Required

    url=gh_repo,  # Optional
    author='weaming',  # Optional
    author_email='garden.yuen@gmail.com',  # Optional

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='rfc alfred efficiency',  # Optional

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    install_requires=[
        'Alfred-Workflow'
    ],  # Optional

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={  # Optional
        'alfred_rfc': ['rfc_list.json'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'alfred-rfc=alfred_rfc.search:main',
        ],
    },

    project_urls={  # Optional
        'Bug Reports': gh_repo,
        'Source': gh_repo,
    },
    )
