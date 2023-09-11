#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import argparse
import glob
import gymnasium as gym
import sys
from rl_zoo3.utils import ALGOS


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test agent on environment')
    parser.add_argument('-n', '--n-timesteps', type=int, default=10000, help='Number of timesteps')
    parser.add_argument('-a', '--agent', type=str, default='a2c', help='Agent type')
    parser.add_argument('-e', '--environment', default='CartPole-v1', help='Specify environment')
    args = vars(parser.parse_args())

    agent_path = glob.glob('/app/out/{}/{}/best_model.zip'.format(args['agent'], args['environment']))
    if len(agent_path) < 1:
        print('No trained model found. Make sure a best_model.zip exists')
        sys.exit(1)

    agent_path = agent_path[0]

    env = gym.make(args['environment'], render_mode='human')
    obs, info = env.reset()

    model = ALGOS[args['agent']].load(agent_path, env=env)

    episode_reward = 0.0
    episode_length = 0

    for i in range(args['n_timesteps']):
        action, state = model.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)

        episode_reward += reward
        episode_length += 1

        if terminated or truncated:
            print('Info:', info)
            print(f"Episode Reward: {episode_reward:.2f}")
            print("Episode Length", episode_length)
            episode_reward = 0.0
            episode_length = 0
            obs, info = env.reset()

    env.close()
