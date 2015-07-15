#!/usr/bin/python

from framework import *

#############################  init  ####################################

frm = framework()

frm.prompt = "frmwrk>"

frm.banner = """
 +-----------------------------+
 [                             ]
 [                             ]
 +-----------------------------+
"""

#############################commands####################################

frm.addCommand("exit",
"""

self.put("warning","Exiting now...")
exit(0)

""","Exit the framework", False)

frm.addCommand("use",
"""

self.variantPrompt = "(%s%s%s%s)"%(self.blue,self.bold,self.cmdArgs[0],self.reset)

""","Example of changing your prompt",True)

frm.addCommand("help",
"""

for i in self.cmdList.keys():
	self.put("success","\t%s     %s"%(i.ljust(32),self.cmdList[i][1]))

""","Display help",False)

frm.addCommand("cat",
"""

self.put("informational","'catting' file %s"%self.cmdArgs)
try:
	print open(self.cmdArgs[0]).read()
except IOError:
	self.put("failure","Failed to open file '%s'"%self.cmdArgs[0])

""","View the contents of a file",True)

frm.addCommand("catdummy","pass","Dummy command",False)

frm.addCommand("psencode",
"""

contents = ""
self.put("informational","Prepping command for powershell execution from file '%s'"%self.cmdArgs[0])
try:
	contents = base64.b64encode(open(self.cmdArgs[0]).read().encode("utf-16-le"))
	self.put("success","powershell.exe -nol -nop -win hidden -enc %s"%contents)
except IOError:
	self.put("failure","Failed to encode file")

""","Encode file and build powershell execution command",True)

frm.addCommand("?",
"""
for i in self.cmdList.keys():
        self.put("success","\t%s     %s"%(i.ljust(32),self.cmdList[i][1]))
""","Display help",False)

#########################################################################

frm.execute()
