# To run this code you need to install the following dependencies:
# pip install google-genai

from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()

def generate(prompt):
    client = genai.Client(
        api_key=os.getenv("apikey"),
    )

    model = "gemini-flash-latest"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""{prompt}"""),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        # thinkingConfig: {
        #     thinkingBudget: -1,
        # },
        tools=tools,
        system_instruction=[
            types.Part.from_text(text="""you are  only farmer assistance,  always answer questions briefly"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
while True:
    userinput= input("\nuser: ")
    generate(userinput)
