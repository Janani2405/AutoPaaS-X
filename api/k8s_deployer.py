import yaml
import subprocess
import os

def generate_deployment_yaml(app_name, cpu_units, ram_mb, image="nginx"):
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": f"{app_name}-deployment"
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app": app_name
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": app_name
                    }
                },
                "spec": {
                    "containers": [{
                        "name": app_name,
                        "image": image,
                        "resources": {
                            "requests": {
                                "cpu": f"{cpu_units}",
                                "memory": f"{ram_mb}Mi"
                            },
                            "limits": {
                                "cpu": f"{cpu_units}",
                                "memory": f"{ram_mb}Mi"
                            }
                        }
                    }]
                }
            }
        }
    }

    os.makedirs("manifests", exist_ok=True)
    path = f"manifests/{app_name}_deployment.yaml"
    with open(path, "w") as f:
        yaml.dump(deployment, f)

    print(f"✅ Deployment YAML generated: {path}")
    return path

def apply_yaml(path):
    try:
        result = subprocess.run(["kubectl", "apply", "-f", path], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Deployment applied successfully.")
        else:
            print("❌ Error applying deployment:\n", result.stderr)
    except FileNotFoundError:
        print("⚠️ 'kubectl' not found. Is it installed and added to PATH?")
