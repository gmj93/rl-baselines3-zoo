#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import argparse
import gymnasium as gym
import os
import pickle
import sys
import yaml

from rl_zoo3.utils import ALGOS
from stable_baselines3.common.env_util import make_vec_env
from tqdm import tqdm
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


def linear_schedule(initial_value: Union[float, str]) -> Callable[[float], float]:
    """
    Linear learning rate schedule.

    :param initial_value: (float or str)
    :return: (function)
    """
    # Force conversion to float
    initial_value_ = float(initial_value)

    def func(progress_remaining: float) -> float:
        """
        Progress will decrease from 1 (beginning) to 0
        :param progress_remaining: (float)
        :return: (float)
        """
        return progress_remaining * initial_value_

    return func


def _preprocess_schedules(hyperparams: Dict[str, Any]) -> Dict[str, Any]:
    # Create schedules
    for key in ["learning_rate", "clip_range", "clip_range_vf", "delta_std"]:
        if key not in hyperparams:
            continue
        if isinstance(hyperparams[key], str):
            schedule, initial_value = hyperparams[key].split("_")
            initial_value = float(initial_value)
            hyperparams[key] = linear_schedule(initial_value)
        elif isinstance(hyperparams[key], (float, int)):
            # Negative value: ignore (ex: for clipping)
            if hyperparams[key] < 0:
                continue
            hyperparams[key] = constant_fn(float(hyperparams[key]))
        else:
            raise ValueError(f"Invalid value for {key}: {hyperparams[key]}")
    return hyperparams


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train model for environment')
    parser.add_argument('--algo', help='RL Algorithm', default='ppo', type=str,
                        required=False, choices=list(ALGOS.keys()))
    parser.add_argument('--env', type=str, default='CartPole-v1',
                        help='environment ID')
    parser.add_argument('-n', '--n-timesteps', default=1e6, type=int,
                        help='Number of timesteps to train')
    parser.add_argument('--eval-episodes', default=100, type=int,
                        help='Episodes to evaluate')
    parser.add_argument('--eval-interval', default=5000, type=int,
                        help='Number of steps to run before an evaluation period')
    args = vars(parser.parse_args())

    with open(os.path.join('hyperparams', args['algo'] + '.yml')) as f:
        hyperparams = yaml.safe_load(f)
        hyperparams = hyperparams.get(args['env'])

    if hyperparams is None:
        print('No hyperparams defined for {} on {}', args['algo'], args['env'])
        sys.exit(0)

    out_dir = 'out/{}/{}'.format(args['algo'], args['env'])
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    env = make_vec_env(args['env'], n_envs=hyperparams['n_envs'])
    eval_env = gym.make(args['env'])

    del hyperparams['n_envs']
    del hyperparams['n_timesteps']

    hyperparams = _preprocess_schedules(hyperparams)

    model = ALGOS[args['algo']](env=env, **hyperparams)

    rounds = int(args['n_timesteps'] / args['eval_interval'])
    progressbar_global = tqdm(ncols=100, total=rounds, desc='Training Progress')
    progressbar = tqdm(ncols=100, total=args['eval_episodes'])
    stats = {}

    for r in range(0, rounds):
        progressbar_global.update(1)
        model.learn(total_timesteps=args['eval_interval'])
        model.save(os.path.join(out_dir, 'model_round_{}.zip'.format(r)))
        stats = []
        progressbar.desc = 'Eval round {}'.format(r)

        obs, info = eval_env.reset()
        terminated, truncated = (False, False)

        eval_episode = 0
        while eval_episode < args['eval_episodes']:
            episode_reward = 0.0
            episode_length = 0

            while True:
                action, state = model.predict(obs)
                obs, reward, terminated, trucated, info = eval_env.step(action)

                episode_reward += reward
                episode_length += 1

                if terminated or truncated or episode_length == 1000:
                    stats.append({'episode': eval_episode,
                                  'reward': episode_reward,
                                  'length': episode_length})
                    episode_reward = 0.0
                    episode_length = 0
                    eval_episode += 1
                    obs, info = eval_env.reset()
                    stats_file = os.path.join(out_dir, 'stats_round_{}.p'.format(r))
                    pickle.dump(stats, open(stats_file, 'wb'))
                    progressbar.update(1)
                    break

        progressbar.reset()
