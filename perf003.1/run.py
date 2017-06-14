from pysys.constants import *
from pysys.basetest import BaseTest
import subprocess, signal, os

class PySysTest(BaseTest):
        def execute(self):
            self.correlatorLog = os.path.join(self.output, 'correlator.log')
            process = subprocess.Popen('correlator -f {}'.format(self.correlatorLog), shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
            self.waitForFile(self.correlatorLog)
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Send the signal to all the process groups

        def validate(self):
                self.assertTrue(True)

