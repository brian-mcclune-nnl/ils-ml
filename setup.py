"""Janken setup script."""

import subprocess

from setuptools import setup


def get_version() -> str:
    """Returns the current version of Janken.

    Returns:
        The current version string for Janken.

    """

    return subprocess.run(
        ['git', 'describe', '--long'],
        stdout=subprocess.POPEN,
    ).stdout.decode().rstrip().lstrip('v').split('-')[0]


setup(
    name='janken',
    version=get_version(),
    author='Brian McClune',
    author_email='brian.mcclune@unnpp.gov',
    description='A rock-paper-scissors image classifier!',
    license='BSD',
    keywords="rock paper scissors guu paa choki janken neural networks",
    packages=['janken'],
    entry_points={'console_scripts': ['janken = janken.__main__:main']},
    include_package_data=True,
    install_requires=[
        'pandas',
        'scipy==1.4.1',
        'tabulate',
        'tensorboard==2.1.0',
        'tensorflow==2.1.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python 3',
        'Programming Language :: Python 3.7',
    ],
)
