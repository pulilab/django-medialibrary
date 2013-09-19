import shutil


class TearDownMixin(object):
    """
    This mixin removes all the test files (and folders) created by the tests
    """

    @classmethod
    def tearDownClass(cls):
        try:
            shutil.rmtree('test_temp')
        except OSError:
            pass


from models import *
from serializers import *
from views import *