import os  # 운영 체제와 상호 작용하기 위함함
from dotenv import load_dotenv  # .env 파일에서 환경 변수를 로드하기 위함함

load_dotenv()  # .env 파일에서 환경 변수 가져옴옴
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
NGROK_URL = os.getenv('NGROK_URL')
URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={NGROK_URL}'  # Telegram 봇 API의 웹훅 URL을 설정

print(URL)  # 설정된 URL을 출력