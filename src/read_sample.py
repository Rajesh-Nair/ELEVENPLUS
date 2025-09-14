import json
import os

base = "data"

print(os.path.join(base,"sample_vocab.jsonl"))

# Open and load the JSON file
with open(os.path.join(base,"sample_vocab.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# Print everything
print(data)
data_new = {}

for key, value in data.items():
    data_new[value["Word"].lower()] = value 

# Print the new dictionary
print(data_new)


with open(os.path.join(base,"sample_vocab.json"), "w", encoding="utf-8") as f:
    json.dump(data_new, f, indent=2, ensure_ascii=False)
