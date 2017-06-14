from pysys.constants import *
from pysys.basetest import BaseTest
import subprocess, signal, os
from pysys.process.helper import ProcessWrapper

class PySysTest(BaseTest):
        def execute(self):
 
            self.outputFile = os.path.join(self.output, 'output.log')
            process = ProcessWrapper('echo', arguments=[],environs=os.environ,workingDir=os.getcwd(), state=FOREGROUND, timeout=None, stdout=subprocess.PIPE)
            process.start()

        def validate(self):
                self.assertTrue(True)

