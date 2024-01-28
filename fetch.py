import json
import yaml
import requests

# Fetching the spec from the running Flask app
response = requests.get('http://127.0.0.1:5000/apispec_1.json')
print(response)
spec_json = response.json()

# Convert JSON to YAML
spec_yaml = yaml.dump(spec_json, default_flow_style=False)

# Save to a file
with open('openapi_spec.yml', 'w') as file:
    file.write(spec_yaml)
