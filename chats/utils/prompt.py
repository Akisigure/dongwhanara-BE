from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import List, Dict
import requests
from time import time

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=api_key)

# Pydantic 모델 정의
class Persona(BaseModel):
    name: str
    age: str = None
    gender: str = None
    job: str = None
    background: str = None
    personality: List[str] = []
    abilities: List[str] = []
    goals: List[str] = []
    values: List[str] = []

# 함수 정의
def get_prompt(title, content):
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": (
                    f"당신은 '{title}'의 주인공을 기반으로 페르소나를 생성하는 AI입니다. "
                    "반드시 아래 JSON 형식으로 응답하세요.\n\n"
                    "```json\n"
                    "{\n"
                    "  \"name\": \"\",\n"
                    "  \"persona\": \"\"  \n"
                    "}\n"
                    "```"
                )
            },
            {
                "role": "user",
                "content": (
                    f"제목: {title}\n"
                    f"내용: {content}\n"
                    "위 내용을 바탕으로 주인공의 페르소나를 한국어 문자열로 생성해 주세요."
                )
            }
        ],
        text_format=Persona,
    )

    persona: Persona = response.output_parsed

    name = persona.name
    data = persona.model_dump()

    return name, data


import os
import time
from django.conf import settings
import requests

def get_cover_img(name, prompt_description):
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
           {
  "role": "system",
  "content": "입력된 정보를 바탕으로 반드시 **어린이에게 어울리는 코믹북 스타일**로 이미지를 생성해줘. 이미지에는 **문자, 언어, 텍스트 요소는 절대 포함되면 안 되며**, 반드시 **주인공 한 명만** 등장해야 해."
            },
            {"role": "user", "content": f'주인공 이름 : {name}, 배경정보: {prompt_description}를 바탕으로 키워드를 뽑아줘.'},
        ],
    )

    keyword = completion.choices[0].message.content
    print('키워드 : ', keyword)
    response = client.images.generate(
        model="dall-e-3",
        prompt=keyword,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    res = requests.get(response.data[0].url)

    filename = f"{name}_{int(time.time())}.png"

    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    with open(file_path, 'wb') as f:
        f.write(res.content)

    return filename

