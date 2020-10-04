from setuptools import setup, find_packages

with open('requirements.txt') as fp:
    required = [line.strip() for line in fp if line.strip() != ""]

setup(
    name='pwnamappy',
    version='0.0.1',
    description='Turn every pwn into pin',
    author='Grigorii Dzhanelidze',
    url='https://github.com/strlght/pwnamappy',
    license='Apache License 2.0',
    install_requires=required,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pwnamappy=pwnamappy.__main__:main'],
    }
)