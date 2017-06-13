from pysys.constants import *
from pysys.basetest import BaseTest
import subprocess

class PySysTest(BaseTest):
        def execute(self):
            process = subprocess.Popen('ls', shell=True, stdout=subprocess.PIPE)
            process.wait()
            self.x=1

        def validate(self):
                self.assertTrue(self.x==1)

