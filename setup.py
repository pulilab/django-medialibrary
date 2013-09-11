import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='django-medialibrary',
    version=__import__('medialibrary').__version__,
    author='Viktor Nagy',
    author_email='v@pulilab.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/pulilab/django-medialibrary',
    license='BSD 3-Clause License, see the LICENSE file for details',
    description=u' '.join(__import__('medialibrary').__doc__.splitlines()).strip(),
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Programming Language :: Python',      
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.rst'),
    test_suite="runtests.runtests",
    zip_safe=False,
    install_requires=[
        'Django>=1.4,<1.6',
        'django-model-utils',
        'django-jsonfield>=0.9.10',
    ],
    download_url='https://github.com/pulilab/django-medialibrary/archive/1.1.0.zip'
)
