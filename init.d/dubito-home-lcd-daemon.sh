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
# /etc/init.d/dubito-home-lcd-daemon

set -e 

export ROOTDIR=/root/test-pi/dubito-home/init.d

. /lib/lsb/init-functions

export HOME
case "$1" in
    start)
        log_daemon_msg "Starting Dubito Home LCD Daemon" "dubito-home-lcd-daemon" || true
        start-stop-daemon --start --quiet -b --pidfile /var/run/dubito-home-lcd.pid --exec $ROOTDIR/dubito-home-lcd-daemon.py
        log_end_msg 0 || true
        ;;
    stop)
        log_daemon_msg "Stopping Dubito Home LCD Daemon" "dubito-home-lcd-daemon" || true
        if start-stop-daemon --stop --quiet --oknodo --pidfile /var/run/dubit-home-lcd.pid; then
            log_end_msg 0 || true
        else
            log_end_msg 1 || true
        fi
        ;;
    *)
        echo "Usage: /etc/init.d/dubito-home-lcd-daemon {start|stop}"
        exit 1
        ;;
esac
exit 0
