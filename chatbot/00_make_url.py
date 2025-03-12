import os  # 운영 체제와 상호 작용하기 위해
import requests  # HTTP 요청을 보내기 위해
from dotenv import load_dotenv  # .env 파일에서 환경 변수를 로드하기 위해

load_dotenv()  # .env 파일에서 환경 변수 가져옴
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'

res = requests.get(URL + '/getUpdates')  # Telegram API에서 업데이트를 가져옴옴
res_dict = res.json()  # 응답을 JSON 형식으로 변환환

user_id = res_dict['result'][0]['message']['from']['id']  # 업데이트에서 첫 번째 메시지의 사용자 ID를 추출
text = res_dict['result'][-1]['message']['text']  # 업데이트에서 마지막 메시지의 텍스트를 추출

requests.get(f'{URL}/sendMessage' + f'?chat_id={user_id}&text={text}')  # 추출한 텍스트로 사용자에게 메시지를 보냄