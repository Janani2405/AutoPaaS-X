import yaml
from datetime import datetime, timedelta

def predict_next_invocation(times):
    """
    Dummy logic: assume uniform 30-minute gaps
    """
    last_time = datetime.strptime(times[-1], "%H:%M")
    predicted_time = last_time + timedelta(minutes=30)
    return predicted_time.strftime("%H:%M")

def create_cronjob_yaml(function_name, times):
    next_time = predict_next_invocation(times)
    hour, minute = map(int, next_time.split(":"))

    cronjob = {
        "apiVersion": "batch/v1",
        "kind": "CronJob",
        "metadata": {
            "name": f"{function_name}-warmup"
        },
        "spec": {
            "schedule": f"{minute} {hour} * * *",
            "jobTemplate": {
                "spec": {
                    "template": {
                        "spec": {
                            "containers": [{
                                "name": "warmup",
                                "image": "curlimages/curl",
                                "args": ["http://your-api/{function_name}/warmup"]
                            }],
                            "restartPolicy": "OnFailure"
                        }
                    }
                }
            }
        }
    }

    with open("manifests/cronjob.yaml", "w") as f:
        yaml.dump(cronjob, f)

    print(f"✅ CronJob generated for {next_time} and saved as manifests/cronjob.yaml")
