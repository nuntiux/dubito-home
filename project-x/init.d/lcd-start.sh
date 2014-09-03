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

set -e 

export ROOTDIR=/root/test-pi/project-x/init.d

. /lib/lsb/init-functions

export HOME
case "$1" in
    start)
	    log_daemon_msg "Starting LCD server" "boot-up-lcd" || true
	    start-stop-daemon --start --quiet -b --pidfile /var/run/lcd.pid --exec $ROOTDIR/boot-up-lcd.py
        log_end_msg 0 || true
        ;;
    stop)
	    log_daemon_msg "Stopping  LCD server" "boot-up-lcd" || true
	    if start-stop-daemon --stop --quiet --oknodo --pidfile /var/run/lcd.pid; then
	        log_end_msg 0 || true
	    else
	        log_end_msg 1 || true
	    fi
        ;;
    *)
        echo "Usage: /etc/init.d/lcd {start|stop}"
        exit 1
        ;;
esac
exit 0
