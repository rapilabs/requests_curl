from setuptools import setup, find_packages

setup(
    name='requests_curl',
    version='0.1.1',
    description='Log curl requests for each call to requests',
    author='David Sanders',
    author_email='dsanders@rapilabs.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
)
