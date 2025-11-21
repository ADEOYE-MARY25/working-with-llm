from openai import OpenAI


# Test the code

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5.1",
    input="Write a short bedtime story about a unicorn."
)

print(response.output_text)
