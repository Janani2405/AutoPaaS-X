import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.losses import MeanSquaredError
import os

MODEL_PATH = "ai/lstm_predictor.keras"

def create_model():
    """Create and compile an LSTM model for resource prediction."""
    model = Sequential([
        Input(shape=(1, 7)),  # Input shape: 7 features over 1 timestep
        LSTM(64, return_sequences=False),
        Dense(32, activation='relu'),
        Dense(2)  # Output: [CPU units, RAM MB]
    ])
    model.compile(optimizer='adam', loss=MeanSquaredError())
    return model

def train_and_save_model():
    """Train the LSTM model on dummy data and save it to disk."""
    # Dummy training dataset: shape (samples, features)
    X = np.array([
        [1, 64, 10, 1, 100, 6, 80],  # OS, Arch, Image, Feature, Users, Hours, Past usage
        [0, 32, 5, 0, 30, 3, 50],
        [1, 64, 20, 1, 200, 10, 90],
        [0, 32, 2, 0, 10, 1, 30]
    ])
    y = np.array([
        [2.0, 2048],  # CPU (cores), RAM (MB)
        [1.0, 1024],
        [3.5, 4096],
        [0.5, 512]
    ])

    # Reshape X to LSTM format: (samples, timesteps, features)
    X = X.reshape((X.shape[0], 1, X.shape[1]))

    model = create_model()
    model.fit(X, y, epochs=100, verbose=0)
    model.save(MODEL_PATH)
    print("✅ LSTM model trained and saved to:", MODEL_PATH)

def predict_resources(input_data):
    """
    Predict CPU and RAM requirements based on input data.

    Parameters:
    input_data (list of 7 floats/ints): [os, arch, image_size, feature, users, usage_hours, past_usage]

    Returns:
    dict: Predicted and clamped values for CPU and RAM.
    """
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()

    if len(input_data) != 7:
        raise ValueError("Expected input: [os, arch, image_size, feature, users, usage_hours, past_usage]")

    # Load and run prediction
    model = tf.keras.models.load_model(MODEL_PATH)
    input_array = np.array(input_data).reshape((1, 1, 7))
    prediction = model.predict(input_array, verbose=0)

    # Raw predictions
    raw_cpu = float(prediction[0][0])
    raw_ram = float(prediction[0][1])

    # Clamp and format safely
    safe_cpu = round(max(0.1, min(raw_cpu, 4.0)), 1)  # Limit CPU between 0.1 and 4.0
    safe_ram = max(32, int(round(raw_ram)))          # Minimum 32Mi RAM

    return {
        "predicted_cpu_units": safe_cpu,
        "predicted_ram_MB": safe_ram
    }
