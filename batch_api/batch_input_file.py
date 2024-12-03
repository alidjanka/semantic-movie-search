import json

with open("./movie_latest.json", 'r') as file:
    data = json.load(file)

def write_jsonl(data, output_file):
    system_prompt = "You are an assistant who generates movie descriptions based on the movie's genre and the kind of mood a person would be in to watch it. For each movie, you will describe what it is (its genre, basic plot) and suggest the ideal mood for watching it (whether the person is in the mood for excitement, intellectual stimulation, nostalgia, etc.). Provide a concise and engaging description of the movie."
    
    with open(output_file, 'w') as f:
        for d in data:
            user_prompt = f"Please generate a movie description for {d['title']} based on its genre and the kind of mood a person would be in to watch it."
            jsonl_entry = {
                "custom_id": str(d['id']),
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": 500
                }
            }
            f.write(json.dumps(jsonl_entry) + '\n')

write_jsonl(data, "batchinput.jsonl")