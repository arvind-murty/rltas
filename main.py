from stable_baselines3 import PPO
from src.env import CourseEnv
import gymnasium as gym

env = CourseEnv()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=200000)

obs, info = env.reset()
for _ in range(0, 500):
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()

    if terminated:
        print("TERMINATED\n\n\n\n")
        obs, info = env.reset()
    if truncated:
        print("TRUNCATED\n\n\n\n")
        obs, info = env.reset()
        
