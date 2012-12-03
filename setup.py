#!/usr/bin/env python
from setuptools import setup, find_packages

META_DATA = dict(
    name='django-jasmine',
    version='1.0.0',
    description='Jasmine Javascript testing integration for Django',
    long_description=open('README.rst').read(),
    author='Lincoln Loop',
    author_email='info@lincolnloop.com',
    url='https://github.com/lincolnloop/django-jasmine',
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Testing',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

if __name__ == "__main__":
    setup(**META_DATA)
