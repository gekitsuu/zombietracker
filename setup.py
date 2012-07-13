from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='zombietracker',
      version=version,
      description="Track all the Zombies!",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='zombies flask mongodb pymongo',
      author='Adam Glenn',
      author_email='gekitsuu@gmail.com',
      url='http://www.snakebytekit.com',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
