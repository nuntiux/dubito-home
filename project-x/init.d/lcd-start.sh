### BEGIN INIT INFO
# Provides: LCD - date / time / ip address
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Liquid Crystal Display
# Description: date / time / ip address
### END INIT INFO
 
#! /bin/sh
# /etc/init.d/lcd
 

export ROOTDIR=/root/test-pi/project-x/init.d
 
export HOME
case "$1" in
    start)
        echo "Starting LCD"
	$ROOTDIR/boot-up-lcd.py 2>&1
    ;;
    stop)
        echo "Stopping LCD"
	$ROOTDIR/stop-lcd.py 2>&1
    ;;
    *)
        echo "Usage: /etc/init.d/lcd {start|stop}"
        exit 1
    ;;
esac
exit 0
