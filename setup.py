from setuptools import setup, find_packages

setup(
    name='randtools',
    version='0.9.0',
    packages=find_packages(),
    url='',
    license='BSD 3-Clause License',
    author='Creative Star Studio',
    author_email='qu20121118@yeah.net',
    description='A Python module for generating random data with various features including random integers, letters, ASCII characters, bytes, floats, booleans, and URLs',
    install_requires=[
        'ping3==4.0.8',
    ],
)
