from pysys.constants import *
from pysys.basetest import BaseTest
import os

class PySysTest(BaseTest):
	def execute(self):
                #self.command = '/usr/bin/echo'
                #self.arguments = ["Hello"]
                #self.environs = os.environ
                #os.execve(self.command, self.arguments, self.environs)
                pass

	def validate(self):
		self.assertTrue(True)
