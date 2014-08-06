nagios_unattended_upgrades_reboot_plugin
========================================

A plugin for nagios on Ubuntu/Debian to alert when unattended_upgrades requires a reboot.


The indication that a reboot is needed is the existence of file '/var/run/reboot-required'.
However, if unattended_upgrades is not installed or configured correctly this file will never
be created and the server will appear as though it never needs a reboot.

Because of this, this plugin also checks that unattended_upgrades is installed and configured
properly and alerts if it is not.


Installation
============
* copy unattended_upgrades.py to /usr/lib/nagios/plugins/unattended_upgrades.py, permissions (755/rwxr-xr-x)
* copy unattended_upgrades.cfg to /etc/nagios-plugins/config/unattended_upgrades.cfg, permissions (644/rw-r--r--)
* update your nagios server config with a new service using command_name 'check_unattended_upgrades'

Example: add the following to /etc/nagios3/conf.d/localhost_nagios2.cfg

    define service{
        use                             generic-service         ; Name of service template to use
        host_name                       localhost
        service_description             Unattended Upgrades
        check_command                   check_unattended_upgrades
        }


