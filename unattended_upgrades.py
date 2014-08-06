#!/usr/bin/python
from __future__ import unicode_literals, print_function
import subprocess, sys, os, re

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

def package_installed(package_name):
    """ @since: 2014-08-04
        @author: Jivan
        @return: True if \a package_name is installed, False if not.
    """
    # command output
    co = subprocess.check_output('dpkg -l {pn} | grep {pn}'.format(pn=package_name), shell=True)
    # search match
    m = re.search(package_name, co)
    ret = True if m else False
    return ret


def config_file_contains(config_filename, content_regex):
    """ @since: 2014-08-04
        @author: Jivan
        @return: True if \a content_regex matches content in \a config_filename.
    """
    # config file object
    cf = open(config_filename, 'r')
    # file contents
    fc = cf.read()
    # search match
    sm = re.search(content_regex, fc, flags=re.MULTILINE)
    ret = bool(sm)
    return ret


try:
    # --- Check that 'update-notifier-common' is installed.
    #    This isn't really necessary on Ubuntu machines, but will remind Debian users that this
    #    package is necessary & other distro admins that they can't use this script.
    if not package_installed('update-notifier-common'):
        print("CRITICAL - Package 'update-notifier-common' missing.  This check is only for Ubuntu/Debian")
        sys.exit(CRITICAL)

    # --- Check that 'unattended-upgrades' is installed.
    if not package_installed('unattended-upgrades'):
        print("CRITICAL - Package 'unattended-upgrades' not installed")
        sys.exit(CRITICAL)

    # --- Check that unattended-upgrades is configured for package list updates.
    # '^\s*' Ensures that the line isn't commented out.
    expected_content_regex = r'^\s*' + re.escape(r'APT::Periodic::Update-Package-Lists "1";')
    config_filename = '/etc/apt/apt.conf.d/10periodic'
    if not config_file_contains(config_filename, expected_content_regex):
        print("CRITICAL - 'unattended-upgrades' is not configured to update package lists")
        sys.exit(CRITICAL)

    # --- Check that unattended-upgrades is configured to install security updates.
    # '^\s*' Ensures that the line isn't commented out
    expected_content_regex = r'^\s*' + re.escape(r'"${distro_id}:${distro_codename}-security";')
    config_filename = '/etc/apt/apt.conf.d/50unattended-upgrades'
    if not config_file_contains(config_filename, expected_content_regex):
        print("CRITICAL - 'unattended-upgrades' is not configured to install security updates")
        sys.exit(CRITICAL)

    # --- Check that unattended-upgrades is configured to install recommended updates.
    # '^\s*' Ensures that the line isn't commented out.
    expected_content_regex = r'^\s*' + re.escape(r'"${distro_id}:${distro_codename}-updates";')
    config_filename = '/etc/apt/apt.conf.d/50unattended-upgrades'
    if not config_file_contains(config_filename, expected_content_regex):
        print("WARNING - 'unattended-upgrades' is not configured to install recommended updates")
        sys.exit(WARNING)

    # --- Check if a reboot is required (by checking for file '/var/run/reboot-required')
    reboot_required = os.path.exists('/var/run/reboot-required')
    if reboot_required:
        print("WARNING - Server requires a reboot")
        sys.exit(WARNING)
    else:
        print("OK - unattended_upgrades is running properly and no reboot is required")
        sys.exit(OK)
except Exception as ex:
    print(ex)
    pass

print("UNKNOWN - Check failed with unknown error")
sys.exit(UNKNOWN)
