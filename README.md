# dumping-files-through-telnet
- downloading files from a server which has no samba or ftp service to local through telnet.
- if size of file to be downloaded is hundreds of KBs, it's would block for a long time.
- if arg is start with '/', downloaded files would be located at your local root directory (e.g. C://), else it would be located at current path.

#### Prerequisite
- python 2.7
- [telnetlib](https://docs.python.org/2/library/telnetlib.html)

#### Usage
edit dump.py, filling in the required fields.
for example, if the telnet host looks like this:
```
telnet osdev1
Red Hat Enterprise Linux Server release 5.6 (Tikanga)
Kernel 2.6.18-238.el5 on an x86_64
login: member
Password:
Last login: Tue Jan  6 09:48:29 from 192.168.81.151
osdev1:<users/member>[81]
```
filling in fields like this:
```python
host = "osdev1"
login_prompt = "login: "
username = "member"
password_prompt = "Password: "
password = "XXXXXXX"
command_prompt = "osdev1:<users/member>"
```
if you want to download all files in "/usr/local/bea/projects/applications/eFPower/css"
```
/usr/local/bea/projects/applications/eFPower/css
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
```
execute dump.py like this:
```
python dump.py /usr/local/bea/projects/applications/eFPower/css
# print
# Total 10 file(s):
#   /usr/local/bea/projects/applications/eFPower/css/img/glyphicons.png
#   /usr/local/bea/projects/applications/eFPower/css/img/error.png
#   /usr/local/bea/projects/applications/eFPower/css/ui/__style__.css
#   /usr/local/bea/projects/applications/eFPower/css/ui/icon.css
#   /usr/local/bea/projects/applications/eFPower/css/ui/screen.css
#   /usr/local/bea/projects/applications/eFPower/css/ui/bootstrap.icon-large.css
#   /usr/local/bea/projects/applications/eFPower/css/ui/b290cb188599f73956fd.css
#   /usr/local/bea/projects/applications/eFPower/css/fonts/icons/entypo.ttf
#   /usr/local/bea/projects/applications/eFPower/css/fonts/icons/entypo.eot
#   /usr/local/bea/projects/applications/eFPower/css/fonts/icons/entypo.woff
# Dumping start:
#   Dumping /usr/local/bea/projects/applications/eFPower/css/img/glyphicons.png...
#   Dumping /usr/local/bea/projects/applications/eFPower/css/img/error.png...
#   Dumping /usr/local/bea/projects/applications/eFPower/css/ui/__style__.css...
#   Dumping /usr/local/bea/projects/applications/eFPower/css/ui/icon.css...
#   Dumping /usr/local/bea/projects/applications/eFPower/css/ui/screen.css...
#   Dumping /usr/local/bea/projects/applications/eFPower/css/ui/bootstrap.icon-large.css...
#   Dumping /usr/local/bea/projects/applications/eFPower/css/ui/b290cb188599f73956fd.css...
#   Dumping /usr/local/bea/projects/applications/eFPower/css/fonts/icons/entypo.ttf...
#   Dumping /usr/local/bea/projects/applications/eFPower/css/fonts/icons/entypo.eot...
#   Dumping /usr/local/bea/projects/applications/eFPower/css/fonts/icons/entypo.woff...
# Done!
```
arg is start with '/', so downloaded files would be located at local root directory (C://):
```
tree C:\usr /f
列出資料夾 PATH
磁碟區序號為 EC1F-D82E
C:\USR
└─local
    └─bea
        └─projects
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
```
arg can be a single file, too:
```
python dump.py logAnalysis/test.txt
# print
# Total 1 file(s):
#   logAnalysis/test.txt
# Dumping start:
#   Dumping logAnalysis/test.txt...
# Done!
```
arg isn't start with '/', so downloaded files would be located at current directory.
