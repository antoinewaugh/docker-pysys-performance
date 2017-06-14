from pysys.constants import *
from pysys.basetest import BaseTest
import subprocess, signal, os
from pysys.process.helper import ProcessWrapper

class PySysTest(BaseTest):
        def execute(self):
            self.outputFile = os.path.join(self.output, 'output.log')
            process = ProcessWrapper(os.path.join(self.input, 'filewrite'), arguments=[self.outputFile] ,environs=os.environ,workingDir=os.getcwd(), state=BACKGROUND, timeout=None)
            process.start()
            self.waitForFile(self.outputFile)
            process.stop()

        def validate(self):
                self.assertTrue(True)

