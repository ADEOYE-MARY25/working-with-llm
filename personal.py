from google import genai
from dotenv import load_dotenv
import os 

load_dotenv()

api = os.getenv("apikey")

client = genai.client(api_key=api)

# persona text
persona = '''
You are loan Assistance , a friendly teacher assistance
Your job:
- Greet politely
- Ask follow-up questions
-Explain school activities in simple language 
- Maintain a calm, professional tone
-Always reply in brief
'''

while True:
    userInput =input("user: ")

    final_prompt = f"{persona}\n\nUser: {userInput}:"
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=final_prompt
    )
    print("nAgent:", response.text, "\n")