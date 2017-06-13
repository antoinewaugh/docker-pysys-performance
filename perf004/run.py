import os
from pysys.constants import *
from pysys.basetest import BaseTest
from pysys.process.helper import ProcessWrapper

class PySysTest(BaseTest):
        def execute(self):
            self.correlatorLog = os.path.join(self.output, 'correlator.log')
            process = ProcessWrapper('correlator -f {}'.format(self.correlatorLog))
            process.start()
            self.waitForFile(self.correlatorLog)
            process.stop()

            self.x=1

        def validate(self):
                self.assertTrue(self.x==1)

