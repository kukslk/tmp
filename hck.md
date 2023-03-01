#WEB

'''#!/bin/bash
nmap 500 |
1 | | s/, /
ports=$( -p- --min-rate= $1 grep ^[0-9] | cut -d '/' -f
tr '\n' ',' sed $/ )
nmap -p$ports -A $'''

#OS
