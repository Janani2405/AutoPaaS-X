from flask import Flask, request, jsonify
from ai.lstm_predictor import predict_resources
from ai.dependency_mediator import resolve_dependencies
from serverless.cronjob_generator import create_cronjob_yaml
from sdn.throttler import enforce_bandwidth_policy
from ai.q_learning import update_q_table_from_feedback


app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 AutoPaaS-X API is running!"

@app.route('/predict_resources', methods=['POST'])
def handle_prediction():
    data = request.json
    required_keys = ["os", "arch", "image_size", "feature", "users", "usage_hours", "historical_usage"]
    input_data = [data[k] for k in required_keys]
    result = predict_resources(input_data)
    return jsonify(result)

@app.route('/resolve_dependencies', methods=['POST'])
def handle_dependencies():
    data = request.json
    requirements = data.get("requirements", [])
    cleaned = resolve_dependencies(requirements)
    return jsonify({"cleaned_requirements": cleaned})

@app.route('/generate_cronjob', methods=['POST'])
def handle_cronjob():
    data = request.json
    function_name = data.get("function_name")
    times = data.get("invocation_times", [])
    create_cronjob_yaml(function_name, times)
    return jsonify({"status": "cronjob.yaml generated", "function": function_name})

@app.route('/enforce_bandwidth', methods=['POST'])
def handle_bandwidth():
    data = request.json
    enforce_bandwidth_policy(data)
    return jsonify({"status": "Bandwidth policy evaluated."})


@app.route('/feedback/resource', methods=['POST'])
def update_q_learning():
    data = request.json
    state = data.get("state")  # 0=underutilized, 1=normal, 2=overloaded
    action = data.get("action")  # 0=scale_down, 1=hold, 2=scale_up
    reward = data.get("reward")  # e.g., +2 if successful, -2 if overloaded again

    update_q_table_from_feedback(state, action, reward)
    return jsonify({"status": "Q-table updated"})

@app.route('/deploy_application', methods=['POST'])
def deploy_app():
    data = request.get_json()
    
    # Step 1: Predict Resources
    predict_input = [data[k] for k in [
        "os", "arch", "image_size", "feature",
        "users", "usage_hours", "historical_usage"
    ]]
    prediction = predict_resources(predict_input)

    # Step 2: Resolve Dependencies
    cleaned_requirements = resolve_dependencies(data.get("requirements", []))

    # Step 3: Warm-up Prediction
    create_cronjob_yaml(data["function_name"], data["invocation_times"])

    # Step 4: Enforce Bandwidth Rules
    enforce_bandwidth_policy(data.get("tenant_bandwidth", {}))

    # Step 5: Generate and Apply Deployment YAML
    from api.k8s_deployer import generate_deployment_yaml, apply_yaml
    path = generate_deployment_yaml(
        data["function_name"],
        prediction["predicted_cpu_units"],
        prediction["predicted_ram_MB"]
    )
    apply_yaml(path)

    return jsonify({
        "status": "Deployed successfully",
        "predicted_resources": prediction,
        "cleaned_requirements": cleaned_requirements
    })


if __name__ == "__main__":
    app.run(debug=True)
