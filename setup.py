from setuptools import setup

setup(name="benfordspy",
      version="0.1",
      description="Benford's Law analysis tools",
      url="https://github.com/nyoshimizu/benfordspy",
      author="Nyoshimizu",
      long_description="Tools for parsing various data sources and applying an"
                       "analysis of their numerical data using Benford's Law.",
      license="LGPL-3+",
      packages=['benfordspy'],
      install_requires=[
          'matplotlib',
          'numpy',
          'openpyxl'
      ],
      test_suite='alltests.py'
      )