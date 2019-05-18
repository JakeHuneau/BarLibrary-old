import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'sqlalchemy',
    'bcrypt',
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'waitress',
    'zope.sqlalchemy',
    'pyramid_tm',
    'pyramid_retry',
    'requests'
    ]

setup(name='BarLibrary',
      version='0.0',
      description='BarLibrary',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='JakeHuneau',
      author_email='',
      url='',
      keywords='bar library',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={},
      install_requires=requires,
      entry_points= {
          'paste.app_factory': [
              'main = barlibrary:main'
          ],
          'console_scripts': [
              'initialize_db = barlibrary.scripts.initializedb:main'
          ]
      }
      )
