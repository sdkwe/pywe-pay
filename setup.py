# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.11'


setup(
    name='pywe-pay',
    version=version,
    keywords='Wechat Weixin Pay',
    description='Wechat Pay Module for Python.',
    long_description=open('README.rst').read(),

    url='https://github.com/sdkwe/pywe-pay',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pywe_pay'],
    py_modules=[],
    install_requires=['pywe_base', 'pywe_exception', 'pywe_sign', 'pywe_utils', 'pywe_xml'],
    include_package_data=True,

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
