import gymnasium as gym

for i in sorted(list(gym.envs.registry.keys())):
    print('  ', i)
