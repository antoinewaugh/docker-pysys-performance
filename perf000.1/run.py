from pysys.constants import *
from pysys.basetest import BaseTest
import subprocess, signal, os
from pysys.process.helper import ProcessWrapper

class PySysTest(BaseTest):
        def execute(self):
            process = ProcessWrapper('/usr/bin/echo', arguments=['sample line'],environs=os.environ,workingDir=os.getcwd(), state=FOREGROUND, timeout=None)
            process.start()

        def validate(self):
                self.assertTrue(True)
