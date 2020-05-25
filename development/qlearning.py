from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
import numpy as np
import pandas as pd

from agent import Agent


class Learner(Agent):
    def __init__(self):
        super().__init__()
        self.Q = {}
        self.last_state = None
        self.last_action = None
        self.learning_rate = .7
        self.discount = .9
        self.epsilon = .9

    def reset_hand(self):
        self.last_state = None
        self.last_action = None

    def get_action(self, state):
        if state in self.Q and np.random.uniform(0, 1) < self.epsilon:
            action = max(self.Q[state], key=self.Q[state].get)
        else:
            action = np.random.choice([])  # TODO
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

        self.Q[self.last_state][self.last_action] = (1 - self.learning_rate) * old + self.learning_rate * (
                    reward + new)

    def get_optimal_strategy(self):
        df = pd.DataFrame(self.Q).transpose()
        df['optimal'] = df.apply(lambda x: 'hit' if x['hit'] >= x['stay'] else 'stay', axis=1)
        return df


class DQNAgent(Learner):
    def __init__(self):
        super().__init__()
        self.learning = True
        self.learning_rate = .1
        self.discount = .1
        self.epsilon = .9
        self.Q = {}
        self.last_state = None
        self.last_action = None
        self.hand = []

        # Create Model
        model = Sequential()

        model.add(Dense(2, init='lecun_uniform', input_shape=(2,)))
        model.add(Activation('relu'))

        model.add(Dense(10, init='lecun_uniform'))
        model.add(Activation('relu'))

        model.add(Dense(4, init='lecun_uniform'))
        model.add(Activation('linear'))

        rms = RMSprop()
        model.compile(loss='mse', optimizer=rms)

        self.model = model

    def get_action(self, state):
        rewards = self.model.predict([np.array([state])], batch_size=1)

        if np.random.uniform(0, 1) < self.epsilon:
            if rewards[0][0] > rewards[0][1]:
                action = 1  # TODO
            else:
                action = 0  # TODO
        else:
            action = np.random.choice([0, 1])  # TODO

        self.last_state = state
        self.last_action = action
        self.last_target = rewards

        return action

    def update(self, new_state, reward):
        rewards = self.model.predict([np.array([new_state])], batch_size=1)
        maxQ = rewards[0][0] if rewards[0][0] > rewards[0][1] else rewards[0][1]
        new = self.discount * maxQ

        if self.last_action == 0:  # TODO
            self.last_target[0][0] = reward + new
        else:
            self.last_target[0][1] = reward + new

        # Update model
        self.model.fit(np.array([self.last_state]), self.last_target, batch_size=1, nb_epoch=1, verbose=0)

    def get_optimal_strategy(self):
        index = []
        for x in range(0, 21):
            for y in range(1, 11):
                index.append((x, y))

        df = pd.DataFrame(index=index, columns=['hit', 'stay'])

        for ind in index:
            outcome = self.model.predict([np.array([ind])], batch_size=1)
            df.loc[ind, 'hit'] = outcome[0][0]
            df.loc[ind, 'stay'] = outcome[0][1]

        df['optimal'] = df.apply(lambda x: 'hit' if x['hit'] >= x['stay'] else 'stay', axis=1)
        return df
