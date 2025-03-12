import os
import requests
import random
from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI, Request

from utils import kospi, openai, langchain

app = FastAPI()

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
URL = f'https://api.telegram.org/bot{TOKEN}'

@app.post("/")
async def read_root(request: Request):
    body = await request.json()  # 요청 본문을 JSON으로 변환환
    
    user_id = body['message']['chat']['id']  # 사용자 ID 추출
    text = body['message']['text']  # 메시지 텍스트 추출

    if text[0] == '/':  # 명령어인지 확인
        if text == '/lotto':  # '/lotto' 명령어 처리
            numbers = random.sample(range(1, 46), 6)  # 랜덤 숫자 생성
            output = str(sorted(numbers))  # 숫자 정렬 후 문자열로 변환
        elif text == '/kospi':  # '/kospi' 명령어 처리
            output = kospi()  # kospi 함수 호출
        else:
            output = 'X'  # 알 수 없는 명령어 처리
    else:
        # output = openai(OPENAI_API_KEY, text)  # OpenAI API 호출 
        output = langchain(text)  # langchain 함수 호출

    requests.get(f'{URL}/sendMessage?chat_id={user_id}&text={output}')  # 메시지 전송

    return body  # 요청 본문 반환