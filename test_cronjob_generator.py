from serverless.cronjob_generator import create_cronjob_yaml

historical_invocations = ["09:00", "09:30", "10:00"]
function_name = "data-cleaner"

create_cronjob_yaml(function_name, historical_invocations)
