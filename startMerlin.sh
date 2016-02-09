#!/bin/bash
killall python
echo "Initial Setup"
scl enable python27
mkfifo /tmp/yowsup
cat > /tmp/yowsup &
mpid=$!
echo "Start YowSup";
/var/www/vhosts/pa-rainbows.com/httpdocs/yowsup-new/yowsup-cli demos -l 31644647579:YjBpMbG8qFA+C+cTZrPpXxhwvck= -y < /tmp/yowsup &

echo "WA Auth";
echo "/L" > /tmp/yowsup

echo "Start Merlin";
python /var/www/vhosts/pa-rainbows.com/httpdocs/merlin/merlin.py
