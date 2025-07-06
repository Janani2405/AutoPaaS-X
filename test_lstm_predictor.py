from ai.lstm_predictor import predict_resources
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 = all logs, 1 = info, 2 = warning, 3 = error

# Input format:
# [os, arch, image_size_GB, feature, number_of_users, avg_usage_hours, historical_usage]
input_data = [1, 64, 12.0, 1, 150, 6.5, 80.0]

result = predict_resources(input_data)

print("🔍 Prediction Result:")
print(result)
