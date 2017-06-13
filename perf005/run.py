from pysys.constants import *
from pysys.basetest import BaseTest
import os
from apama.correlator import CorrelatorHelper

class PySysTest(BaseTest):
        def execute(self):
            correlator = CorrelatorHelper(self)
            correlator.start(logfile='correlator.log', waitForServerUp=True)
            self.waitForFile(os.path.join(self.output, 'correlator.log'))
 
            self.x=1

        def validate(self):
                self.assertTrue(self.x==1)

