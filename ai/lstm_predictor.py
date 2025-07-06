import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.losses import MeanSquaredError
import os

MODEL_PATH = "ai/lstm_predictor.keras"

def create_model():
    model = Sequential([
        Input(shape=(1, 7)),              # Fix input_shape warning
        LSTM(64, return_sequences=False),
        Dense(32, activation='relu'),
        Dense(2)  # Output: [CPU units, RAM MB]
    ])
    model.compile(optimizer='adam', loss=MeanSquaredError())  # Fix 'mse' error
    return model

def train_and_save_model():
    # Dummy training data (7 features)
    X = np.array([
        [1, 64, 10, 1, 100, 6, 80],
        [0, 32, 5, 0, 30, 3, 50],
        [1, 64, 20, 1, 200, 10, 90],
        [0, 32, 2, 0, 10, 1, 30]
    ])
    y = np.array([
        [2.0, 2048],
        [1.0, 1024],
        [3.5, 4096],
        [0.5, 512]
    ])

    X = X.reshape((X.shape[0], 1, X.shape[1]))

    model = create_model()
    model.fit(X, y, epochs=100, verbose=0)
    model.save(MODEL_PATH)  # Let Keras infer the format
    print("✅ LSTM model trained and saved to:", MODEL_PATH)

def predict_resources(input_data):
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()

    if len(input_data) != 7:
        raise ValueError("Expected input: [os, arch, image_size, feature, users, usage_hours, past_usage]")

    model = tf.keras.models.load_model(MODEL_PATH)
    input_array = np.array(input_data).reshape((1, 1, 7))
    prediction = model.predict(input_array, verbose=0)
    return {
        "predicted_cpu_units": round(float(prediction[0][0]), 2),
        "predicted_ram_MB": int(prediction[0][1])
    }
