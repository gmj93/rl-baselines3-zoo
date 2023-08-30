# General info

Build non-official container:

```
cd Docker
docker build --tag=rl_zoo3 .
```

# Train model for env

```
./train_model_env.py -a <agent_name> -e <env_name> -n <n_timesteps>
```