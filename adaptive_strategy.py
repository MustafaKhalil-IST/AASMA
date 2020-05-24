import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop

STATE_SIZE, ACTION_SIZE = 17, 1


class ActionSelection:
    eGreedy = 1
    softMax = 2


class LearningApproach:
    QLearning = 1
    SARSA = 2


class AdaptiveStrategy:
    def __init__(self, player):
        super().__init__("adaptive", player)
        self.action_selection = ActionSelection.softMax
        self.learning_approach = LearningApproach.QLearning
        self.Q = {}
        self.learning_rate = .7
        self.discount = .9
        self.epsilon = .9
        self.last_state = None
        self.last_action = None

    def getQ(self, s, a):
        if s in self.Q:
            if a in self.Q[str(s)]:
                return self.Q[str(s)][a]
            else:
                return 0
        else:
            return 0

    def reset_hand(self):
        self.last_state = None
        self.last_action = None

    def get_action(self, state):
        if state in self.Q and np.random.uniform(0, 1) < self.epsilon:
            action = max(self.Q[state], key=self.Q[state].get)
        else:
            action = np.random.choice(state[-4:])
            if state not in self.Q:
                self.Q[state] = {}
            self.Q[state][action] = 0

        self.last_state = state
        self.last_action = action

        return action

    def update(self, new_state, reward):
        old = self.Q[self.last_state][self.last_action]

        if new_state in self.Q:
            new = self.discount * self.Q[new_state][max(self.Q[new_state], key=self.Q[new_state].get)]
        else:
            new = 0

        self.Q[self.last_state][self.last_action] = (1 - self.learning_rate) * old + self.learning_rate * (reward + new)
