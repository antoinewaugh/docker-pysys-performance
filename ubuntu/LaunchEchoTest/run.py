from pysys.constants import *
from pysys.basetest import BaseTest
import subprocess, signal, os
from pysys.process.helper import ProcessWrapper

class PySysTest(BaseTest):
        def execute(self):
            process = ProcessWrapper('/usr/bin/echo', arguments=[],environs=os.environ,workingDir=os.getcwd(), state=FOREGROUND, timeout=None, stdout='/dev/null')
            process.start()

        def validate(self):
            self.assertTrue(True)

