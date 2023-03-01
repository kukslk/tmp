#WEB

'ports=$( -p- --min-rate= $1 | grep ^[0-9] | cut -d "/" -f 1 | tr "\n" "," | sed $//)'

#OS
