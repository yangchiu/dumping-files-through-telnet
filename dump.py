
import telnetlib
import sys
import re
import os

end_of_line = "\r\n"
host = ""   
login_prompt = ""
username = ""
password_prompt =  ""
password = ""
command_prompt = ""

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

# (6) logout
tn.write("exit" + end_of_line)
print "Done!"
