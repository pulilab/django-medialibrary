#!/usr/bin/env python
import sys, os

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.auth',
            'medialibrary',
        ),
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        SITE_ID=1,
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
        ROOT_URLCONF = 'medialibrary.urls',
        TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'
    )

from medialibrary import utils
from django.db import models
utils.content_type_restriction = models.Q(app_label='auth', model='user')

from django.test.utils import get_runner


def setup_test_route(instance, filename=None):
    return 'test_temp/%s' % filename
utils.setup_upload_route = setup_test_route


def runtests():
    os.environ['FORCE_DB'] = '1'
    if len(sys.argv) > 1:
        totest = map(lambda m: 'medialibrary.tests.%s' % m, sys.argv[1:])
    else:
        totest = ['medialibrary', ]
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(totest)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()

