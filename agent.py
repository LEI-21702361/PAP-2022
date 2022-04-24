import gym
import argparse
import ns3gym
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from wjwgym.agents import DDPGBase
from wjwgym.models import SimpleCriticNet
import os
CUDA = torch.cuda.is_available()

class OUProcess(object):

    def __init__(self, x_size, mu=0, theta=0.15, sigma=0.3):
        self.x = np.ones(x_size) * mu
        self.x_size = x_size
        self.mu = mu
        self.theta = theta
        self.sigma = sigma

    def noise(self):
        dx = self.theta * (self.mu - self.x) + self.sigma * np.random.randn(self.x_size)
        self.x = self.x + dx
        return self.x


class DDPG(DDPGBase):
    def _build_net(self):
      
        n_states, n_actions = self.n_states, self.n_actions
        print('bound: ', self.bound)
        if CUDA:
            print(f'use pytorch with gpu')
        else:
            print(f'use pytorch with cpu')
        self.actor_eval = ActorNetwork(n_states, n_actions, a_bound=self.bound)
        self.actor_target = ActorNetwork(n_states, n_actions, a_bound=self.bound)
        self.critic_eval = SimpleCriticNet(n_states, n_actions, n_neurons=64)
        self.critic_target = SimpleCriticNet(n_states, n_actions, n_neurons=64)

    def _build_noise(self):
        self.noise = OUProcess(self.n_actions, sigma=0.1)

    def get_action_noise(self, state, rate=1):
        action = self.get_action(state)
        noise_rate = max(self.bound * rate, 1)
        action_noise = self.noise.noise() * noise_rate 
        action = np.clip(action + action_noise, 0.01, None)
      
        return action

    def learn_batch(self):
        if 'learn_step' not in self.__dict__:
            self.learn_step = 0
        c_loss, a_loss = self.learn()
        if c_loss is not None:
            self.summary_writer.add_scalar('c_loss', c_loss, self.learn_step)
            self.summary_writer.add_scalar('a_loss', a_loss, self.learn_step)
            self.learn_step += 1

   
    def save(self, episode):
        state = {
            'actor_eval_net': self.actor_eval.state_dict(),
            'actor_target_net': self.actor_target.state_dict(),
            'critic_eval_net': self.critic_eval.state_dict(),
            'critic_target_net': self.critic_target.state_dict(),
            'episode': episode,
            'learn_step': self.learn_step
        }
        torch.save(state, './drlte.pth')

   
    def load(self):

            return 0
        saved_state = torch.load("./drlte.pth")
        self.actor_eval.load_state_dict(saved_state['actor_eval_net'])
        self.actor_target.load_state_dict(saved_state['actor_target_net'])
        self.critic_eval.load_state_dict(saved_state['critic_eval_net'])
        self.critic_target.load_state_dict(saved_state['critic_target_net'])
        self.learn_step = saved_state['learn_step']
        return saved_state['episode'] + 1


class ActorNetwork(nn.Module):
    def __init__(self, n_states, n_actions, n1_neurons=64, n2_neurons=32, a_bound=None):
        """
        @param n_obs: number of observations
        @param n_actions: number of actions
        @param n1_neurons: 
        @param n2_neurons: 
        @param a_bound: action
        """
        super(ActorNetwork, self).__init__()
        self.bound = a_bound if a_bound else n_actions * 2
        self.fc1 = nn.Linear(n_states, n1_neurons)
        self.fc1.weight.data.normal_(0, 0.1)
        self.fc2 = nn.Linear(n1_neurons, n2_neurons)
        self.fc2.weight.data.normal_(0, 0.1)
        self.out = nn.Linear(n2_neurons, n_actions)
        self.out.weight.data.normal_(0, 0.1)
        if CUDA:
            self.bound = torch.FloatTensor([self.bound]).cuda()
        else:
            self.bound = torch.FloatTensor([self.bound])

    def forward(self, x):
      
        x = x.cuda() if CUDA else x
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.out(x)
        action_value = F.softmax(x, dim=1)
        action_value = action_value * self.bound
        return action_value

env = gym.make('ns3-v0')
env.reset()
agent = MyAgent()
ob_space = env.observation_space


print("Observation space: ", ob_space,  ob_space.dtype)

stepIdx = 0

except KeyboardInterrupt:
    print("Ctrl-C -> Exit")
finally:
    env.close()
    print("Done")