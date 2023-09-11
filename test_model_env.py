#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import argparse
import os
import subprocess


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
    parser = argparse.ArgumentParser(description='Test model for environment')
    parser.add_argument('-n', '--n-timesteps', type=int, default=-1, help='Number of timesteps')
    parser.add_argument('-a', '--agent', type=str, default='a2c', help='Agent type')
    parser.add_argument('-e', '--environment', default='', help='Specify single environment')
    args = vars(parser.parse_args())

    defs = Definitions()

    test_cmd = ['docker', 'run', '-it', '--rm', '-e', 'DISPLAY=$DISPLAY',
                '-v', '/tmp/.X11-unix:/tmp/.X11-unix',
                '-v', '{}:/app:rw'.format(defs.RLZOO_PATH),
                defs.DOCKER_IMG, 'python3', '/app/test.py', '-a', args['agent'],
                '-e', args['environment']]

    if args['n_timesteps'] != -1:
        test_cmd.append('-n')
        test_cmd.append(str(args['n_timesteps']))

    # Printing the command while I don't find a way to run it directly from the script
    print('\n', ' '.join(test_cmd))
