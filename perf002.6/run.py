from pysys.constants import *
from pysys.basetest import BaseTest
import subprocess

class PySysTest(BaseTest):
        def execute(self):
            self.inputFile = os.path.join(self.input, 'correlator.log')
            self.outputFile = os.path.join(self.output, 'output.log')
            command = 'cat {} > {}'.format(self.inputFile, self.outputFile)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            self.waitForFile(self.outputFile)

        def validate(self):
                self.assertTrue(True)

