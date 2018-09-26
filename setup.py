import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'colander',
    'deform',
    'bcrypt',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_tm',
    'sqlalchemy',
    'pyramid_debugtoolbar',
    'waitress',
    'zope.sqlalchemy'
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
]

setup(name='money_map',
      version='0.0',
      description='money_map',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Lauri Elias',
      author_email='laurileet@gmail.com',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = money_map:main
      [console_scripts]
      initialize_money_map_db = money_map.initialize_db:main
      """,
      )
