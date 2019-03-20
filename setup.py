#!/usr/bin/env python

from subprocess import check_call

from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist

install_requires = [
    'PyQt5',
    'numpy',
    'psutil',
    'scikit-image',
    'opencv-python-headless',
    'imctools',
    'pyqtgraph>=0.11'
]

dependency_links = [
    'git+https://github.com/pyqtgraph/pyqtgraph',
    'git+https://github.com/BodenmillerGroup/imctools.git'
]

cmdclass = {}

try:
    from pyqt_distutils.build_ui import build_ui


    class build_res(build_ui):
        """Build UI, resources and translations."""

        def run(self):
            # build UI & resources
            build_ui.run(self)


    cmdclass['build_res'] = build_res
except ImportError:
    pass


class custom_sdist(sdist):
    """Custom sdist command."""

    def run(self):
        self.run_command('build_res')
        sdist.run(self)


cmdclass['sdist'] = custom_sdist


class bdist_app(Command):
    """Custom command to build the application. """

    description = 'Build the application'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('build_res')
        check_call(['pyinstaller', '-y', 'setup/histoslider.spec'])


cmdclass['bdist_app'] = bdist_app

setup(name='histoslider',
      version="0.0.1.dev1",
      packages=find_packages(),
      description='HistoSlider viewer app',
      author='Anton Rau',
      author_email='anton.rau@uzh.ch',
      license='MIT',
      url='https://github.com/BodenmillerGroup/HistoSlider',
      python_requires=">=3.7",
      install_requires=install_requires,
      dependency_links=dependency_links,
      entry_points={
          'gui_scripts': [
              'histoslider = histoslider.app:main'
          ]
      },
      cmdclass=cmdclass)
