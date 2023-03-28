"""
Install audiomd
"""

from setuptools import setup, find_packages
from version import get_version


def main():
    """Install audiomd"""
    setup(
        name='audiomd',
        packages=find_packages(exclude=['tests', 'tests.*']),
        version=get_version(),
        install_requires=[
            'lxml',
        ]
    )


if __name__ == '__main__':
    main()
