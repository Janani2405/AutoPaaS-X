from ai.q_learning import train_q_learning, get_scaling_decision

train_q_learning()  # Train and save the Q-table

# Test decisions
for state in range(3):
    decision = get_scaling_decision(state)
    print(f"State {state}: {decision}")
