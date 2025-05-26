from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

# def test_client():
#     response = client.responses.create(
#         model="gpt-4o-mini",
#         input="Write a one-sentence bedtime story about a unicorn."
#     )

#     print(response.output_text)