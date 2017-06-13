import os
from pysys.constants import *
from pysys.basetest import BaseTest
from pysys.process.helper import ProcessWrapper
#from apama.common import ApamaServerProcess, _allocateUniqueProcessStdOutErr
	
class PySysTest(BaseTest):
        def execute(self):
            self.correlatorLog = os.path.join(self.output, 'correlator.log')

            process = ProcessWrapper('/home/antoine/softwareag/Apama/bin/correlator', arguments=['-f', self.correlatorLog],environs=os.environ,workingDir=os.getcwd(), state=BACKGROUND, timeout=None)
            process.start()
            self.waitForFile(self.correlatorLog)
            process.stop()

            self.x=1

        def validate(self):
                self.assertTrue(self.x==1)

