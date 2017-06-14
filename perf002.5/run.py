from pysys.constants import *
from pysys.basetest import BaseTest
import subprocess

class PySysTest(BaseTest):
        def execute(self):
            self.outputFile = os.path.join(self.output, 'output.log')
            process = subprocess.Popen('echo "." > {}'.format(self.outputFile), shell=True, stdout=subprocess.PIPE)
            process.wait()
            self.waitForFile(self.outputFile)

        def validate(self):
                self.assertTrue(True)

