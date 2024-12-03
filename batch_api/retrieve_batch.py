from openai import OpenAI
import json
import pandas as pd
client = OpenAI()

file_response = client.files.content("file-5VmEe6FXcGuAy8nMwc36zk")
jsonl_text = file_response.text

data = []
for line in jsonl_text.strip().split('\n'):
    record = json.loads(line)  # Parse JSON from each line
    custom_id = record.get('custom_id')
    content = record['response']['body']['choices'][0]['message']['content']
    data.append({'custom_id': custom_id, 'content': content})

# Create a Pandas DataFrame from the extracted data
df = pd.DataFrame(data)

with open("movies_latest.json", 'r') as file:
    full_data = json.load(file)

for movie in full_data:   
    content = df[df['custom_id'] == movie['id']]['content'].values[0]
    movie['description'] = content

with open('movies_latest_2.json', 'w') as json_file:
    json.dump(full_data, json_file, indent=4)