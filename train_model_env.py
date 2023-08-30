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
    parser = argparse.ArgumentParser(description='Train model for environment')
    parser.add_argument('-n', '--n-timesteps', type=int, default=-1, help='Number of timesteps')
    parser.add_argument('-a', '--agent', type=str, default='a2c', help='Agent type')
    parser.add_argument('-e', '--environment', default='', help='Specify single environment')
    parser.add_argument('-l', '--list-envs', action='store_true', help='List environments')
    parser.add_argument('-k', '--list-agents', action='store_true', help='List agents')
    args = vars(parser.parse_args())

    defs = Definitions()

    if args['list_envs']:
        output = run_command(['docker', 'run', '-i', '--rm', '-v', '{}:/app:rw'.format(defs.RLZOO_PATH),
                              defs.DOCKER_IMG, 'python3', '/app/get_envs.py'])
        print(output)
        sys.exit(0)

    if args['list_agents']:
        output = run_command(['docker', 'run', '-i', '--rm', '-v', '{}:/app:rw'.format(defs.RLZOO_PATH),
                              defs.DOCKER_IMG, 'python3', '/app/get_agents.py'])
        print(output)
        sys.exit(0)

    train_cmd = ['docker', 'run', '-i', '--rm', '-v', '{}:/app:rw'.format(defs.RLZOO_PATH),
                 defs.DOCKER_IMG, 'python3', '/app/train.py', '--algo', args['agent'],
                 '--env', args['environment'], '-f', '/app/rl-trained-agents']

    if args['n_timesteps'] != -1:
        train_cmd.append('-n')
        train_cmd.append(str(args['n_timesteps']))

    process = subprocess.Popen(train_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, bufsize=1, universal_newlines=True)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line, end='')
