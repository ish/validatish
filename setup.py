from setuptools import setup, find_packages
import sys, os

version = '0.6.1'

setup(name='validatish',
      version=version,
      description="Validatish is a minimal library of validators that can validate in a functional or class instantiated style.",
      long_description="""\
      Validatish is a simple validation library designed to be a good building block for validation structures. It implements some basic validators in functional form (i.e. simple function calls) or in class form (i.e. instantiate a class and then just call the validate method). Have a look at the project site at `http://validat.ish.io <http://validat.ish.io>`_

      Changlog at `http://github.com/ish/validatish/raw/master/CHANGELOG <http://github.com/ish/validatish/raw/master/CHANGELOG>`_
""",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Environment :: Web Environment",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ], 
      keywords='validation schema forms form library form validate validator check checker',
      author='Tim Parkin, Matt Goodall',
      author_email='developers@ish.io',
      url='http://validat.ish.io',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite='validatish.tests',
      )
