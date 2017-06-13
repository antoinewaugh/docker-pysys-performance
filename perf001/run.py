from pysys.constants import *
from pysys.basetest import BaseTest

class PySysTest(BaseTest):
        def execute(self):
                self.x=1

        def validate(self):
                self.assertTrue(self.x==1)

