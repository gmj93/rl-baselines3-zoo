# Running interactive docker

docker run -it --privileged=true --rm -e DISPLAY=$DISPLAY --name=rl_zoo3 -v /tmp/.X11-unix:/tmp/.X11-unix -v /workspace/dev/rl-baselines3-zoo_gmj/:/app:rw rl_zoo3 tmux

# Training

python3 train.py --algo a2c --env MountainCarContinuous-v0 --eval-freq 10000 --eval-episodes 20 --n-eval-envs 1 --save-freq 100000 -n 2000000


python3 -m rl_zoo3.benchmark --no-hub

