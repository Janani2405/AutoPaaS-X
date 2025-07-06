# import os
# os.environ["TRANSFORMERS_NO_TF_WARNING"] = "1"
# os.environ["USE_TF"] = "1"  # Force TensorFlow backend

# from transformers import pipeline

# # Load a lightweight model using TensorFlow backend
# classifier = pipeline("sentiment-analysis", framework="tf")

REPLACEMENTS = {
    "tensorflow==2.9.0": "tensorflow==2.12.0",
    "torch==1.7.0": "torch==2.0.0",
    "scipy==1.3.0": "scipy==1.11.0"
}

KNOWN_CONFLICTS = {
    "tensorflow==2.9.0",
    "torch==1.7.0",
    "scipy==1.3.0"
}

def resolve_dependencies(requirements_list):
    cleaned_requirements = []
    for line in requirements_list:
        if line in KNOWN_CONFLICTS:
            replacement = REPLACEMENTS.get(line)
            if replacement:
                print(f"🔁 Replaced: {line} → {replacement}")
                cleaned_requirements.append(replacement)
            else:
                print(f"⚠️ Removed incompatible package: {line}")
        else:
            cleaned_requirements.append(line)
    return cleaned_requirements
