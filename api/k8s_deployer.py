import yaml
import subprocess
import os

def generate_deployment_yaml(app_name, cpu_units, ram_mb, image="nginx"):
    # 🔒 Clamp and format CPU/RAM
    safe_cpu = str(round(max(0.1, min(cpu_units, 4.0)), 1))     # CPU: 0.1 to 4.0 cores
    safe_ram = f"{max(32, int(ram_mb))}Mi"                      # RAM: ≥ 32Mi

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
                                "cpu": safe_cpu,
                                "memory": safe_ram
                            },
                            "limits": {
                                "cpu": safe_cpu,
                                "memory": safe_ram
                            }
                        }
                    }]
                }
            }
        }
    }

    # 📝 Save to YAML
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
