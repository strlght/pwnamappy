from setuptools import setup, find_packages

with open("README.md", "rb") as f:
    long_description = f.read().decode("utf-8")

with open('requirements.txt') as fp:
    required = [line.strip() for line in fp if line.strip() != ""]

setup(
    name='pwnamappy',
    version='0.0.1',
    description='Turn pwns into pins',
    long_description=long_description,
    author='Grigorii Dzhanelidze',
    url='https://github.com/strlght/pwnamappy',
    license='Apache License 2.0',
    install_requires=required,
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pwnamappy=pwnamappy.__main__:main'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
