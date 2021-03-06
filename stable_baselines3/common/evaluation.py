# Copied from stable_baselines
import numpy as np

from stable_baselines3.common.vec_env import VecEnv


def evaluate_policy(model, env, n_eval_episodes=10, deterministic=False,
                    render=False, callback=None, reward_threshold=None,
                    return_episode_rewards=False, **kwargs):  # plot_results =False
    """
    Runs policy for ``n_eval_episodes`` episodes and returns average reward.
    This is made to work only with one env.

    :param model: (BaseRLModel) The RL agent you want to evaluate.
    :param env: (gym.Env or VecEnv) The gym environment. In the case of a ``VecEnv``
        this must contain only one environment.
    :param n_eval_episodes: (int) Number of episode to evaluate the agent
    :param deterministic: (bool) Whether to use deterministic or stochastic actions
    :param render: (bool) Whether to render the environment or not
    :param callback: (callable) callback function to do additional checks,
        called after each step.
    :param reward_threshold: (float) Minimum expected reward per episode,
        this will raise an error if the performance is not met
    :param return_episode_rewards: (bool) If True, a list of reward per episode
        will be returned instead of the mean.
    :return: (float, float) Mean reward per episode, std of reward per episode
        returns ([float], [int]) when ``return_episode_rewards`` is True
    """
    if isinstance(env, VecEnv):
        assert env.num_envs == 1, "You must pass only one environment when using this function"

    episode_rewards, episode_lengths = [], []
    for _ in range(n_eval_episodes):
        try:
            obs = env.reset(env_seed= kwargs['env_seed']) #if not(env_seed ==-1) else env.reset()
        except:
            obs = env.reset ()
        done, state = False, None
        episode_reward = 0.0
        episode_length = 0
        while not done:
            action, state = model.predict(obs, state=state, deterministic=deterministic)
            obs, reward, done, _info = env.step(action, **kwargs)#, plot_before_reset=plot_results)
            episode_reward += reward
            if callback is not None:
                callback(locals(), globals())
            episode_length += 1
            if render:
                env.render()
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)
    if reward_threshold is not None:
        assert mean_reward > reward_threshold, ('Mean reward below threshold: '
                                                f'{mean_reward:.2f} < {reward_threshold:.2f}')
    if return_episode_rewards:
        return episode_rewards, episode_lengths
    return mean_reward, std_reward


def evaluate_baseline(env, n_eval_episodes=1, deterministic=True,
                    render=False, callback=None, reward_threshold=None,
                    return_episode_rewards=False, **kwargs):  # plot_results =False
    """
    Runs policy for ``n_eval_episodes`` episodes and returns average reward.
    This is made to work only with one env.

    :param model: (BaseRLModel) The RL agent you want to evaluate.
    :param env: (gym.Env or VecEnv) The gym environment. In the case of a ``VecEnv``
        this must contain only one environment.
    :param n_eval_episodes: (int) Number of episode to evaluate the agent
    :param deterministic: (bool) Whether to use deterministic or stochastic actions
    :param render: (bool) Whether to render the environment or not
    :param callback: (callable) callback function to do additional checks,
        called after each step.
    :param reward_threshold: (float) Minimum expected reward per episode,
        this will raise an error if the performance is not met
    :param return_episode_rewards: (bool) If True, a list of reward per episode
        will be returned instead of the mean.
    :return: (float, float) Mean reward per episode, std of reward per episode
        returns ([float], [int]) when ``return_episode_rewards`` is True
    """
    if isinstance(env, VecEnv):
        assert env.num_envs == 1, "You must pass only one environment when using this function"

    episode_rewards, episode_lengths = [], []
    for _ in range(n_eval_episodes):
        try:
            obs = env.reset(env_seed=kwargs['env_seed'], C_ALGO=kwargs['C_ALGO'], no_of_users_list=kwargs['no_of_users_list'])#C_algo=C_algo,seed=env_seed)
        except:
            obs = env.reset (env_seed=kwargs['env_seed'], C_ALGO=kwargs['C_ALGO'])
            #obs = env.reset (**kwargs)

        done, state = False, None
        episode_reward = 0.0
        episode_length = 0
        while not done:
            dummy_action = np.array([-1])
            obs, reward, done, _info = env.step(dummy_action, **kwargs)#, plot_before_reset=plot_results)
            #obs, reward, done, _info = env.step (dummy_action)  # , plot_before_reset=plot_results)
            episode_reward += reward
            if callback is not None:
                callback(locals(), globals())
            episode_length += 1
            if render:
                env.render()
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)
    if reward_threshold is not None:
        assert mean_reward > reward_threshold, ('Mean reward below threshold: '
                                                f'{mean_reward:.2f} < {reward_threshold:.2f}')
    if return_episode_rewards:
        return episode_rewards, episode_lengths
    return mean_reward, std_reward
