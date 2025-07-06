from api.k8s_deployer import generate_deployment_yaml, apply_yaml

# Simulated prediction values
cpu = 0.5
ram = 256
app_name = "autoscaler-demo"

yaml_path = generate_deployment_yaml(app_name, cpu, ram)
apply_yaml(yaml_path)

