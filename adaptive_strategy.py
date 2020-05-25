import numpy as np
import pandas as pd
from strategy import Strategy


def encode_card(card):
    code = 0
    if card[1] == 'H':
        code = 1 * 13
    if card[1] == 'S':
        code = 2 * 13
    if card[1] == 'D':
        code = 3 * 13
    if card[1] == 'C':
        code = 4 * 13
    code = code + card[0]
    return code


def encode_state(table, hand):
    hand = [encode_card(card) for card in hand]
    if len(hand) != 13:
        hand += (13 - len(hand)) * [0]
    table = [encode_card(card) for card in table]
    if len(table) != 4:
        table += (4 - len(table)) * [0]
    res = hand + table
    return np.array(res)


class ActionSelection:
    eGreedy = 1
    softMax = 2


class LearningApproach:
    QLearning = 1
    SARSA = 2


class Adaptive(Strategy):
    def __init__(self, player):
        super().__init__("adaptive", player)
        self.player = player
        self.action_selection = ActionSelection.softMax
        self.learning_approach = LearningApproach.QLearning
        self.Q = {}
        self.learning_rate = .7
        self.discount = .9
        self.epsilon = .9
        self.last_state = None
        self.last_action = None
        self.last_reward = -10

    def original_state(self):
        return encode_state(self.player.table, self.player.hand)

    def get_actions(self):
        return np.array([encode_card(card) for card in self.player.determine_selectable_cards(self.player.table)])

    def reward(self, state, action):
        if len(self.player.table) != 3:
            return 0
        else:
            return 1 if self.player.points[-1] == 1 else -1

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

    def setQ(self, state, action, v):
        if str(state) in self.Q:
            self.Q[str(state)][action] = v
        else:
            self.Q[str(state)] = {}
            self.Q[str(state)][action] = v

    def getQ(self, state, action):
        if str(state) in self.Q:
            if action in self.Q[str(state)]:
                return self.Q[str(state)][action]
            else:
                return 0
        else:
            return 0

    def updateQ(self, new_state, reward):
        new_state = encode_state(new_state["table"], new_state["hand"])
        old = self.getQ(self.last_state, self.last_action)
        new = 0
        if str(new_state) in self.Q:
            max_action_q = -1
            for action in self.Q[str(new_state)]:
                if max_action_q > self.Q[str(new_state)][action]:
                    max_action_q = self.Q[str(new_state)][action]
            new = self.discount * max_action_q
        self.setQ(self.last_state, self.last_action,
                  (1 - self.learning_rate) * old + self.learning_rate * (reward + new))

    def get_best_action(self, state, selectable):
        if str(state) in self.Q:
            max_action, max_q = None, -10000
            for action in self.Q[str(state)]:
                if action in selectable:
                    if max_q > self.Q[str(state)][action]:
                        max_action, max_q = action, self.Q[str(state)][action]
            return max_action if max_action is not None else selectable[np.random.choice(range(len(selectable)))]
        else:
            return selectable[np.random.choice(range(len(selectable)))]

    def play(self, selectable, round):
        self.last_state = self.original_state()
        chosen = self.get_best_action(self.last_state, selectable)
        self.last_action = encode_card(chosen)
        return chosen
