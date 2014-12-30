 vi  /home/nunpa/IBLBadges/badges/setup.py ; sudo -u edxapp /edx/bin/pip.edxapp install /home/nunpa/IBLBadges/badges;sudo /edx/bin/supervisorctl -c /edx/etc/supervisord.conf restart edxapp:;tail -f /edx/var/log/supervisor/cmstderr.log

