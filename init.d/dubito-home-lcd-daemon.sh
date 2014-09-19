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
#
# Samuel Pasquier - samuel@happycoders.org
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# /etc/init.d/dubito-home-lcd-daemon

set -e 

export ROOTDIR=/root/dubito-home/init.d

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
