import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()


setup(name='projectksi',
      version='0.0',
      description='projectksi',
      long_description=README + '\n\n' +  CHANGES,
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
      dependency_links = [
          'https://github.com/psychowico/pyramid_viewscomposer/tarball/master#egg=pyramid_viewscomposer',
      ],
      install_requires=[
          'pyramid',
          'pyramid_jinja2',
          'pyramid_debugtoolbar',
          'pyramid_viewscomposer',
          'waitress',
          'six'
      ],
      #I not stored this list in variable, because PyCharm don't see dependencies in this situation
      tests_require=[
          'pyramid',
          'pyramid_jinja2',
          'pyramid_debugtoolbar',
          'pyramid_viewscomposer',
          'waitress',
          'six'
      ],
      test_suite="projectksi",
      entry_points = """\
      [paste.app_factory]
      main = projectksi:main
      """,
      )

