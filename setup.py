import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()


setup(name='projectksi',
      version='0.0',
      description='projectksi',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      dependency_links=[
          'https://github.com/psychowico/pyramid_viewscomposer/tarball/master#egg=pyramid_viewscomposer',
          'https://github.com/psychowico/Squeezeit/tarball/master#egg=squeezeit',
          #oursql for python 3 version
          'https://launchpad.net/oursql/py3k/py3k-0.9.3/+download/oursql-0.9.3.zip#egg=oursql-0.9.3',
      ],
      install_requires=[
          'pyramid',
          'pyramid_tm',
          'SQLAlchemy >= 0.7.8',
          #mysql driver
          'oursql == 0.9.3',
          'zope.sqlalchemy',
          'pyramid_jinja2',
          'pyramid_debugtoolbar',
          'pyramid_viewscomposer',
          'waitress',
          'six',
          'squeezeit',
          'lesscss'
      ],
      #I'm not stored this list in variable, because PyCharm IDE don't see dependencies in this situation (genius)
      tests_require=[
          'pyramid',
          'pyramid_tm',
          'SQLAlchemy >= 0.7.8',
          'oursql == 0.9.3',
          'zope.sqlalchemy',
          'pyramid_jinja2',
          'pyramid_debugtoolbar',
          'pyramid_viewscomposer',
          'waitress',
          'six',
          'squeezeit',
          'lesscss'
      ],
      test_suite="projectksi",
      entry_points = """\
      [paste.app_factory]
      main = projectksi:main
      """,
      )

