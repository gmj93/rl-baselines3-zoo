#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import argparse
import os
import subprocess
import sys


class Definitions(object):
    DOCKER_IMG = 'rl_zoo3'
    RLZOO_PATH = os.getcwd()


def run_command(command):
    try:
        output = subprocess.check_output(command)
        return output.decode('utf-8')
    except subprocess.CalledProcessError:
        print('WARNING: error executing "{}"'.format(command))
    except Exception as e:
        print('WARNING: exception {}'.format(e))
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the container and returns a command to enter')
    parser.add_argument('-s', '--stop', action='store_true', help='Stop container')
    args = vars(parser.parse_args())

    if args['stop']:
        run_command(['docker', 'stop', 'rl-zoo'])
        sys.exit(0)

    defs = Definitions()
    output = run_command(['docker', 'run', '-dit', '--rm', '--name=rl-zoo',
                          '--privileged=true', '-e', 'DISPLAY=$DISPLAY',
                          '-v', '/tmp/.X11-unix:/tmp/.X11-unix',
                          '-v', '{}:/app:rw'.format(defs.RLZOO_PATH),
                          defs.DOCKER_IMG, '/bin/bash'])

    print('docker exec -it -e DISPLAY=$DISPLAY rl-zoo /bin/bash')
