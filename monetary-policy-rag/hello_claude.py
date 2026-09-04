import os
from anthropic import Anthropic

# The SDK automatically looks for ANTHROPIC_API_KEY in the environment,
# so we don't even have to pass it explicitly — but being explicit once,
# here, proves to you that it's actually being read correctly.
api_key = os.environ["ANTHROPIC_API_KEY"]

client = Anthropic(api_key=api_key)

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello in one short sentence."}
    ]
)
print(response.content[0].text)