# _*_ coding: utf8 _*_

import os
import sys

from platform import dist


class OperationalSystem(object):

    '''
    Class about operational system attributes.
    '''

    # Distro family constants (tuple)
    RH_FAMILY = ('redhat', 'centos')
    DEB_FAMILY = ('debian', 'ubuntu', 'linuxmint')

    def __init__(self):
        self.distro = dist()[0].lower()
        self.disto_version = dist()[1]
        self.distro_family = ''

        try:
            if self.distro in self.RH_FAMILY:
                self.distro_family = 'rh'
            elif self.distro in self.DEB_FAMILY:
                self.distro_family = 'deb'
            else:
                raise ValueError
        except:
            print('Error: Distro not supported!')
            sys.exit(1)


def systemd_compat():
    # Function to test SystemD compatibility

    CMD = 'command -v systemctl > /dev/null'
    RESULT = os.system(CMD)

    try:
        if RESULT != 0:
            raise ValueError
    except:
        print('Error: Only for SystemD systems based!')
        sys.exit(1)


def add_user_and_group(user='postgres', group='postgres', verbose=False):
    # System group for PostgreSQL
    cmd = 'groupadd -r {} &> /dev/null'.format(group)
    os.system(cmd)

    # System user for PostgreSQL
    cmd = (
        'useradd -s /bin/bash '
        '-k /etc/skel '
        '-d /var/lib/pgsql '
        '-g {} -m -r {}  &> /dev/null'.format(user, group)
        )
    os.system(cmd)


def main():
    # Main Function

    my_system = OperationalSystem()
    systemd_compat()


if __name__ == '__main__':
    print('Coming soon...')
