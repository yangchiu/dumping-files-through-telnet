dumping-files-through-telnet
============================
C:\Users\pychiu>tree C:\usr /f
列出資料夾 PATH
磁碟區序號為 EC1F-D82E
C:\USR
└─local
    └─bea
        └─projects
            └─efaraday
                └─applications
                    └─eFPower
                        └─css
                            ├─fonts
                            │  └─icons
                            │          entypo.eot
                            │          entypo.ttf
                            │          entypo.woff
                            │
                            ├─img
                            │      error.png
                            │      glyphicons.png
                            │
                            └─ui
                                    b290cb188599f73956fd.css
                                    bootstrap.icon-large.css
                                    icon.css
                                    screen.css
                                    __style__.css

ftcosdev1:<applications/eFPower>[96] tree /usr/local/bea/projects/efaraday/applications/eFPower/css
/usr/local/bea/projects/efaraday/applications/eFPower/css
|-- fonts
|   `-- icons
|       |-- entypo.eot
|       |-- entypo.ttf
|       `-- entypo.woff
|-- img
|   |-- error.png
|   `-- glyphicons.png
`-- ui
    |-- __style__.css
    |-- b290cb188599f73956fd.css
    |-- bootstrap.icon-large.css
    |-- icon.css
    `-- screen.css

4 directories, 10 files

Red Hat Enterprise Linux Server release 5.6 (Tikanga)
Kernel 2.6.18-238.el5 on an x86_64
login: member
Password:
Last login: Tue Jan  6 09:48:29 from 192.168.81.151

ftcosdev1:<users/member>[81]

'''
For download files from linux server via Telnet.

if size of file to be downloaded is hundreds of KBs, 
it's would block for a long time.

if arg is start with '/',
downloaded files would be located at your local root directory (e.g. C://),
else it would be located at C://user//$username

'''

import telnetlib
import sys
import re
import os

end_of_line = "\r\n"
host = "ftcosdev1"
login_prompt = "login: "
username = ""
password_prompt = "Password: "
password = ""
command_prompt = "ftcosdev1:<users/member>"

target = sys.argv[1]

tail = "tail " + target + end_of_line
find = "find " + target + " -type f" + end_of_line

regex = re.compile(r'[^0-9a-f]')

# (1) login
tn = telnetlib.Telnet(host)
tn.read_until(login_prompt)
tn.write(username + end_of_line)
tn.read_until(password_prompt)
tn.write(password + end_of_line)
tn.read_until(command_prompt)

# (2) test if a directory
directory = False
tn.write(tail)
res = tn.read_until(command_prompt)
if " Is a directory" in res:
  directory = True

# (3) list files to be downloaded
files = []
if not directory:
  files.append(target)
else:
  tn.write(find)
  s = tn.read_until(command_prompt)
  s = s.split(end_of_line)
  for sub in reversed(s):
  	if target not in sub:
  	  continue
  	elif sub.index(target) != 0:
  	  continue
  	files.append(sub)

# (4) print files to be downloaded
print "Total " + str(len(files)) + " file(s):"
for sub in files:
  print "  " + sub

print "Dumping start:"

# (5) dumping start!
for f in files:

  print "  Dumping " + f + "..."

  # (5.1) hexdump file in files
  od = "od -tx1 " + f + end_of_line
  tn.write(od)
  res = tn.read_until(command_prompt)

  res = res.replace(end_of_line, " ").split(" ")

  for ele in reversed(res):
    if len(ele) != 2:
      res.remove(ele)
    elif regex.search(ele) is not None:
  	  res.remove(ele)

  s = ''
  for ele in res:
    s += ele
  s = s.decode('hex')

  # (5.2) check folder exists in local
  dir = os.path.dirname(f)
  if not os.path.exists(dir):
    os.makedirs(dir)

  # (5.3) create file in local
  bin = open(f, 'wb')
  bin.write(s)
  bin.close()


tn.write("exit" + end_of_line)
print "Done!"

C:\Users\pychiu>python dump.py /usr/local/bea/projects/efaraday/applications/eFPower/css
Total 10 file(s):
  /usr/local/bea/projects/efaraday/applications/eFPower/css/img/glyphicons.png
  /usr/local/bea/projects/efaraday/applications/eFPower/css/img/error.png
  /usr/local/bea/projects/efaraday/applications/eFPower/css/ui/__style__.css
  /usr/local/bea/projects/efaraday/applications/eFPower/css/ui/icon.css
  /usr/local/bea/projects/efaraday/applications/eFPower/css/ui/screen.css
  /usr/local/bea/projects/efaraday/applications/eFPower/css/ui/bootstrap.icon-large.css
  /usr/local/bea/projects/efaraday/applications/eFPower/css/ui/b290cb188599f73956fd.css
  /usr/local/bea/projects/efaraday/applications/eFPower/css/fonts/icons/entypo.ttf
  /usr/local/bea/projects/efaraday/applications/eFPower/css/fonts/icons/entypo.eot
  /usr/local/bea/projects/efaraday/applications/eFPower/css/fonts/icons/entypo.woff
Dumping start:
  Dumping /usr/local/bea/projects/efaraday/applications/eFPower/css/img/glyphicons.png...
  Dumping /usr/local/bea/projects/efaraday/applications/eFPower/css/img/error.png...
  Dumping /usr/local/bea/projects/efaraday/applications/eFPower/css/ui/__style__.css...
  Dumping /usr/local/bea/projects/efaraday/applications/eFPower/css/ui/icon.css...
  Dumping /usr/local/bea/projects/efaraday/applications/eFPower/css/ui/screen.css...
  Dumping /usr/local/bea/projects/efaraday/applications/eFPower/css/ui/bootstrap.icon-large.css...
  Dumping /usr/local/bea/projects/efaraday/applications/eFPower/css/ui/b290cb188599f73956fd.css...
  Dumping /usr/local/bea/projects/efaraday/applications/eFPower/css/fonts/icons/entypo.ttf...
  Dumping /usr/local/bea/projects/efaraday/applications/eFPower/css/fonts/icons/entypo.eot...
  Dumping /usr/local/bea/projects/efaraday/applications/eFPower/css/fonts/icons/entypo.woff...
Done!

C:\Users\pychiu\dump>python dump.py logAnalysis/test.txt
Total 1 file(s):
  logAnalysis/test.txt
Dumping start:
  Dumping logAnalysis/test.txt...
Done!
