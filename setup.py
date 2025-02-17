# -*- coding: utf-8 -*-
import setuptools
from setuptools import setup, find_packages

setup(
    name='facebook-graphql-scraper',
    version='1.1.2',
    packages=[
        "fb_graphql_scraper",
        "fb_graphql_scraper.pages",
        "fb_graphql_scraper.base",
        "fb_graphql_scraper.tests", 
        "fb_graphql_scraper.utils",
        ],
    license='MIT',
    description='Implement Facebook scraper for post data retrieval',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='FaustRen',
    author_email='faustren1z@gmail.com',
    url='https://github.com/FaustRen/FB_graphql_scraper',
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)