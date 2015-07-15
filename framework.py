#!/usr/bin/python
import base64, sys, time, readline

class framework:

	def __init__(self):
                self.red    = "\033[91m"
                self.yellow = "\033[93m"
                self.green  = "\033[92m"
                self.blue   = "\033[94m"
		self.purple   = "\033[95m"
                self.reset  = "\033[0m"
                self.bold   = "\033[1m"

		self.prompt        = ">"
		self.variantPrompt = ""
		self.failureIcon = "[-]"
		self.failureColor = self.red

		self.warningIcon = "[!]"
		self.warningColor = self.yellow

		self.statusIcon  = "[*]"
		self.statusColor = self.blue

		self.successIcon = "[+]"
		self.successColor = self.green

		self.informationalIcon = "[*]"
		self.informationalColor = self.purple

		self.exitMsg = "Exiting now..."
		self.banner = "= Framework Banner ="

		self.cmdList = {}

		self.addCommand("exit","self.doExit()","Exit the framework",False)

		self.imports = []

	def complete(self, text, state):
		for cmd in self.cmdList.keys():
			if cmd.lower().startswith(text.lower()):
				if not state:
					return cmd
				else:
					state -= 1
	def execute(self):
		currentCmd = ""
		print self.banner
		while True:
			try:
				readline.parse_and_bind("tab: complete")
				readline.set_completer(self.complete)
				currentCmd = raw_input("%s%s "%(self.variantPrompt,self.prompt))
				#print "debug: %s"%currentCmd
				self.executeCommand(currentCmd)
			except KeyboardInterrupt:
				print "\r",
				self.put("warning",self.exitMsg)
				exit(0)

	def put(self,event,txt):
		event = event.lower()
		if event == "status":
			print "%s%s%s%s %s"%(self.getColor("status"),self.getColor("bold"),self.statusIcon,self.getColor("reset"),txt)			
		elif event == "success":
			print "%s%s%s%s %s"%(self.getColor("success"),self.getColor("bold"),self.successIcon,self.getColor("reset"),txt)			
		elif event == "failure":
			print "%s%s%s%s %s"%(self.getColor("failure"),self.getColor("bold"),self.failureIcon,self.getColor("reset"),txt)
		elif event == "warning":
			print "%s%s%s%s %s"%(self.getColor("warning"),self.getColor("bold"),self.warningIcon,self.getColor("reset"),txt)			
		elif event == "informational":
			print "%s%s%s%s %s"%(self.getColor("informational"),self.getColor("bold"),self.informationalIcon,self.getColor("reset"),txt)			

		else:
			print "%s"%(txt)

	def getColor(self,status):
		status = status.lower()
		if status == "warning":
			return self.warningColor
		elif status == "failure":
			return self.failureColor
		elif status == "success":
			return self.successColor
		elif status == "status":
			return self.statusColor
		elif status == "informational":
			return self.informationalColor
		elif status == "reset":
			return self.reset
		elif status == "bold":
			return self.bold
		else:
			return ""

	def addCommand(self,cmd,functionality,desc,requiresArg):
		self.cmdList[cmd.lower()] = (functionality,desc,requiresArg)

	def executeCommand(self,cmd):
		if cmd != "":
			if ((len(cmd.split()) > 1) and (cmd.split()[0].lower() in self.cmdList.keys())): 	# for commands with args
				if (self.cmdList[cmd.split()[0].lower()][2] == True):
					#self.put("informational","DEBUG: You have provided a command that has an arg")
					self.cmdArgs = cmd.split()[1:]
					exec(self.cmdList[cmd.split()[0].lower()][0])
					#for i in self.cmdArgs:
					#	self.put("informational","debug: %s"%i)

			elif (len(cmd.split()) == 1) and (cmd.lower() in self.cmdList.keys()):  		# for commands without args
				if (self.cmdList[cmd.lower()][2] == False):
					#self.put("informational","DEBUG: You have provided an argless command")
					exec(self.cmdList[cmd.lower()][0])
