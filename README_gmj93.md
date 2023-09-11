# General info

This is for personal use only and not intended to replace the official resources.

Build non-official container:

```
cd Docker
docker build --tag=rl_zoo3 .
```

# Train model for env

```
./train_model_env.py -a <agent_name> -e <env_name> -n <n_timesteps>
```

# Test model

```
./test_model_env.py -a <agent_name> -e <env_name> -n <n_timesteps>
```