from openai import OpenAI
client = OpenAI()

print(client.batches.retrieve("batch_674dfcba191081909b1ba58c8a434145"))