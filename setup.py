# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sentinel_engine',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.3.1',

    description='Sentinel-Engine allows searching,' \
               + 'downloading and processing Sentinel data',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/pypa/sampleproject',
    author='George Petrakis',
    author_email='gkpetrak@gmail.com',
    license='GPL',
    classifiers=[
        "Development Status :: 3 - Alpha"],

    keywords='',
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
    # To install data files
    include_package_data=True, 

    install_requires=[
      # # The commented name next to the package
      # # is the Ubuntu 16.04 package that provides it
      # # with version in parenthesis

      # # Apps with official Ubuntu 16.04 packages
 
      "sentinelsat==0.7.3",
      "gdal==1.11.2",
      "schedule>=0.4.3",
],
)

