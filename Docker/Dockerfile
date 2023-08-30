FROM ubuntu:jammy
LABEL Description="RL-Baselines3-Zoo"

RUN apt update && apt upgrade -y && apt install -y \
	autoconf \
	build-essential \
	cmake \
	curl \
	git \
	htop \
	iptables \
	libssl-dev \
	libtool \
	pkg-config \
	python3 \
	python3-opengl \
	python3-pip \
	tmux \
	vim \
	wget \
	x11-utils \
	xvfb && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install \
	box2d \
	box2d-py \
	gym \
	gymnasium[all] \
	huggingface_hub \
	huggingface_sb3 \
	numpy \
	optuna \
	pyaml \
	pygame \
	pyglet \
	pytablewriter \
	rich \
	sb3_contrib \
	stable-baselines3 \
	swig \
	tqdm \
	zmq

ENV DISPLAY=:99
CMD Xvfb $DISPLAY -screen 0 1024x768x16 +extension RANDR -listen tcp &>/dev/null &

COPY tmux.conf /root/.tmux.conf

CMD ["bash"]