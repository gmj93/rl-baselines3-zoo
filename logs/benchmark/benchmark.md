
## Performance of trained agents

Final performance of the trained agents can be found in the table below.
This was computed by running `python -m rl_zoo3.benchmark`:
it runs the trained agent (trained on `n_timesteps`) for `eval_timesteps` and then reports the mean episode reward
during this evaluation.

It uses the deterministic policy except for Atari games.

You can view each model card (it includes video and hyperparameters)
on our Huggingface page: https://huggingface.co/sb3

*NOTE: this is not a quantitative benchmark as it corresponds to only one run
(cf [issue #38](https://github.com/araffin/rl-baselines-zoo/issues/38)).
This benchmark is meant to check algorithm (maximal) performance, find potential bugs
and also allow users to have access to pretrained agents.*

"M" stands for Million (1e6)

|algo |         env_id         |mean_reward|std_reward|n_timesteps|eval_timesteps|eval_episodes|
|-----|------------------------|----------:|---------:|-----------|-------------:|------------:|
|a2c  |Acrobot-v1              |    -83.353|    17.213|500k       |        149979|         1778|
|a2c  |CartPole-v1             |    500.000|     0.000|500k       |        150000|          300|
|a2c  |LunarLander-v2          |    155.751|    80.419|200k       |        149443|          297|
|a2c  |LunarLanderContinuous-v2|     84.225|   145.906|5M         |        149305|          256|
|ars  |Acrobot-v1              |    -82.884|    23.825|500k       |        149985|         1788|
|ars  |CartPole-v1             |    500.000|     0.000|50k        |        150000|          300|
|ars  |LunarLander-v2          |    -66.375|   168.323|2M         |        149899|         1096|
|ars  |LunarLanderContinuous-v2|    167.959|   147.071|2M         |        149883|          562|
|ddpg |LunarLanderContinuous-v2|    230.217|    92.372|300k       |        149862|          556|
|dqn  |Acrobot-v1              |    -76.639|    11.752|100k       |        149998|         1932|
|dqn  |CartPole-v1             |    500.000|     0.000|50k        |        150000|          300|
|dqn  |LunarLander-v2          |    154.382|    79.241|100k       |        149373|          200|
|ppo  |Acrobot-v1              |    -73.506|    18.201|1M         |        149979|         2013|
|ppo  |CartPole-v1             |    500.000|     0.000|100k       |        150000|          300|
|ppo  |LunarLander-v2          |    242.119|    31.823|1M         |        149636|          369|
|ppo  |LunarLanderContinuous-v2|    270.863|    32.072|1M         |        149956|          526|
|qrdqn|Acrobot-v1              |    -69.135|     9.967|100k       |        149949|         2138|
|qrdqn|CartPole-v1             |    500.000|     0.000|50k        |        150000|          300|
|qrdqn|LunarLander-v2          |     70.236|   225.491|100k       |        149957|          522|
|sac  |LunarLanderContinuous-v2|    260.390|    65.467|500k       |        149634|          672|
|td3  |LunarLanderContinuous-v2|    207.451|    67.562|300k       |        149488|          337|
|tqc  |LunarLanderContinuous-v2|    277.956|    25.466|500k       |        149928|          706|
|trpo |Acrobot-v1              |    -83.114|    18.648|100k       |        149976|         1783|
|trpo |CartPole-v1             |    500.000|     0.000|100k       |        150000|          300|
|trpo |LunarLander-v2          |    133.166|   112.173|200k       |        149088|          230|
|trpo |LunarLanderContinuous-v2|    262.387|    21.428|100k       |        149925|          501|
