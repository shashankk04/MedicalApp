import json

with open('API_key.json', 'r') as f:
    keys = json.load(f)

print(keys)