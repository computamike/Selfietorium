#
# Regular cron jobs for the selfietorium package
#
0 4	* * *	root	[ -x /usr/bin/selfietorium_maintenance ] && /usr/bin/selfietorium_maintenance
