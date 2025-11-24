# To run this code you need to install the following dependencies:
# pip install google-genai

from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

class Request(BaseModel):
    message: str



load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            types.Part.from_text(text="""you are only farmer assistance,  always answer questions briefly"""),
        ],
    )
    output= ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
       output += chunk.text
    return output


@app.get("/")
def root():
    return { "message": "Welcome to MaryAI"}


@app.get("/health")
def healthcheck():
    return { "message": "MaryAI in good health and ready to chat"}


@app.post("/chat")
def chat(prompt: Request):
    userinput= prompt.message
    response=generate(userinput) 
    return response
