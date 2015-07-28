#!/usr/bin/python
import sys, urllib

def usage():
	print("[!] usage: %s <requestFile>"%sys.argv[0])
	print("[!]  turns a raw POST request file into a html form")
	exit(-1)

if not (len(sys.argv) == 2):
	usage()

infile = sys.argv[1]
inContents = ""
inList = []
formurl = ""

try:
	inContents = open(infile).read()
except IOError:
	print "[!] error reading file '%s', exiting..."%infile
	exit(-1)

inList	 = inContents.split("\n")
formData = urllib.unquote(inList[-1]).split("&")
host	 = ""

for line in inList:
	if line.lower().startswith("host: "):
		host = line[5:].strip()
		break

if (inList[0].startswith("POST")):
	formurl = inList[0].split(" ")[1].strip() # get the url the request is going to

output = []
output.append("<HTML>")
output.append('<form method=POST name="frm1" action="http://%s%s">'%(host,formurl))

for field in formData:
	output.append('<input type="hidden" name="%s" value="%s">'%(field.split("=")[0],field.split("=")[1]))

output.append("</form>")
output.append("</html>")

for x in output:
	print x
