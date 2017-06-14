import os
from pysys.constants import *
from pysys.basetest import BaseTest
from pysys.process.helper import ProcessWrapper
#from apama.common import ApamaServerProcess, _allocateUniqueProcessStdOutErr
	
class PySysTest(BaseTest):
        def execute(self):
            self.correlatorLog = os.path.join(self.output, 'correlator.log')
            process = ProcessWrapper(os.path.join(os.environ['APAMA_HOME'],'bin','correlator'), arguments=[],environs=os.environ,workingDir=os.getcwd(), state=BACKGROUND, timeout=None, stdout=self.correlatorLog)
            process.start()
            self.waitForFile(self.correlatorLog)
            process.stop()


        def validate(self):
                self.assertTrue(1==1)

