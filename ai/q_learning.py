import numpy as np
import random
import os
import pickle

Q_TABLE_FILE = "ai/q_table.pkl"

# States: 0=underutilized, 1=normal, 2=overloaded
# Actions: 0=scale_down, 1=hold, 2=scale_up
NUM_STATES = 3
NUM_ACTIONS = 3
LEARNING_RATE = 0.1
DISCOUNT = 0.9
EPSILON = 0.2  # Exploration rate

# Reward mapping: [state][action]
REWARD_MATRIX = [
    [1, -1, -5],  # underutilized
    [-2, 2, -2],  # normal
    [-5, -2, 2]   # overloaded
]

def init_q_table():
    if os.path.exists(Q_TABLE_FILE):
        with open(Q_TABLE_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return np.zeros((NUM_STATES, NUM_ACTIONS))

def save_q_table(q_table):
    with open(Q_TABLE_FILE, "wb") as f:
        pickle.dump(q_table, f)

def train_q_learning(episodes=1000):
    q_table = init_q_table()
    
    for _ in range(episodes):
        state = np.random.choice(NUM_STATES)
        if random.uniform(0, 1) < EPSILON:
            action = np.random.choice(NUM_ACTIONS)
        else:
            action = np.argmax(q_table[state])

        reward = REWARD_MATRIX[state][action]
        next_state = state  # For simplicity, assume environment doesn’t change in this mock setup

        q_table[state][action] = q_table[state][action] + LEARNING_RATE * (
            reward + DISCOUNT * np.max(q_table[next_state]) - q_table[state][action]
        )

    save_q_table(q_table)
    print("✅ Q-learning training complete and Q-table saved.")

def get_scaling_decision(state):  # state = 0, 1, or 2
    q_table = init_q_table()
    action_index = np.argmax(q_table[state])
    actions = ["scale_down", "hold", "scale_up"]
    return actions[action_index]

def update_q_table_from_feedback(current_state, action_taken, reward):
    q_table = init_q_table()

    old_value = q_table[current_state][action_taken]
    next_max = np.max(q_table[current_state])  # assume same state (for simplicity)

    # Q-learning update rule
    new_value = old_value + LEARNING_RATE * (reward + DISCOUNT * next_max - old_value)
    q_table[current_state][action_taken] = new_value

    save_q_table(q_table)
    print(f"📈 Q-table updated for state={current_state}, action={action_taken}")
