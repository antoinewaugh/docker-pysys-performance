import os
from pysys.constants import *
from pysys.basetest import BaseTest
from pysys.process.helper import ProcessWrapper
	
class PySysTest(BaseTest):
        def execute(self):
            self.correlatorLog = os.path.join(self.output, 'correlator.log')
            process = ProcessWrapper(os.path.join(os.environ['APAMA_HOME'],'bin','correlator'), arguments=['-f', self.correlatorLog],environs=os.environ,workingDir=os.getcwd(), state=BACKGROUND, timeout=None)
            process.start()
            self.waitForFile(self.correlatorLog)
            process.stop()


        def validate(self):
                self.assertTrue(1==1)

