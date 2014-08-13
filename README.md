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

For a local check:
* copy unattended_upgrades.cfg to /etc/nagios-plugins/config/unattended_upgrades.cfg, permissions (644/rw-r--r--)
* update your nagios host config with a new service using command_name 'check_unattended_upgrades'

Example: add the following to /etc/nagios3/conf.d/localhost_nagios2.cfg

    define service{
        use                             generic-service         ; Name of service template to use
        host_name                       localhost
        service_description             Unattended Upgrades
        check_command                   check_unattended_upgrades
        }

For a remote check:
* Add the following line to /etc/nagios/nrpe_local.cfg (or /etc/nagios/nrpe.cfg if you don't have one).
    command[check_unattended_upgrades]=/usr/lib/nagios/plugins/unattended_upgrades.py
* update your nagios remote host config with a new service to perform 'check_unattended_upgrades' via check_nrpe.
Example: add the following to /etc/nagios3/conf.d/<my remote host>.cfg
    define service{
        use				generic-service
	host_name			<my remote host>
	service_description		Unattended Upgrades
	check_command			check_nrpe_1arg!check_unattended_upgrades
	}

Of course nrpe must be installed and configured on the remote machine.  In Ubuntu this is as simple as
installing package 'nagios-nrpe-server' and updating /etc/nagios/nrpe.cfg with 'allowed_hosts=127.0.0.1,<my nagios server ip>'.

