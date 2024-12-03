import openai

client = openai.OpenAI()

batch_input_file = client.files.create(
  file=open("/home/alican/Desktop/Projects/semantic-movie-search/batch_api/batchinput.jsonl", "rb"),
  purpose="batch"
)

batch_input_file_id = batch_input_file.id

response = client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": "movie descriptions"
    }
)

print(response) 