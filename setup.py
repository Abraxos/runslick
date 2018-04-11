'''Setup file for runslick'''
from setuptools import setup, find_packages


with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

setup(
    name='runslick',
    version='0.1.0',
    description='A highly configurable program launcher',
    long_description=README,
    author='Eugene Kovalev',
    author_email='eugene@kovalev.systems',
    url='https://github.com/Abraxos/runslick',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={'console_scripts': ['runslick=runslick.core:main']},
    install_requires=REQUIREMENTS,
)
