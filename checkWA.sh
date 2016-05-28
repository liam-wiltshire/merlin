#!/bin/bash
processes=`ps aux | grep "yowsup-cli" | wc -l`
echo $processes
if [[ "$processes" == "2" ]]; then
	echo "WA is running";
else
	echo "WA is dead";
	(scl enable python27 "/var/www/vhosts/pa-rainbows.com/httpdocs/yowsup-new/yowsup-cli demos -l 31644647579:YjBpMbG8qFA+C+cTZrPpXxhwvck= -y < /tmp/yowsup > /tmp/yowlog" ) &
	sleep 5 ;
	echo "/L" > /tmp/yowsup
fi

tgprocesses=`ps aux | grep "telegram-cli" | wc -l`
echo $tgprocesses
if [[ "$tgprocesses" == "2" ]]; then
	echo "TG is running";
else
	echo "TG is dead";
	/var/www/vhosts/pa-rainbows.com/httpdocs/tg/bin/telegram-cli -R -W -P 4458 -k /var/www/vhosts/pa-rainbows.com/httpdocs/tg/server.pub --json &
fi
