from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
import requests

f = open("./slack.key")
lines = f.readlines()
SLACK_BOT_TOKEN = lines[0].strip()
SLACK_SIGNING_SECRET = lines[1].strip()
SLACK_APP_LEVEL = lines[2].strip()
f.close()

f = open("./exchange.key")
lines = f.readlines()
EXCHANGE_KEY = lines[0].strip()
f.close()

# Slack Bolt 앱과 FastAPI 앱 생성
slack_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
app = FastAPI()
handler = SlackRequestHandler(app=slack_app)

# 슬랙 이벤트 엔드포인트
@app.post("/slack/events")
async def endpoint(req: Request):
    return await handler.handle(req)

# 'hello' 메시지에 반응하는 핸들러 등록
@slack_app.message("hello")
def reply_hello(message, say):
    print('haha', message, say)
    user_id = message['user']
    say(f'hello <@{user_id}>님')

# '야야' 메시지에 반응하는 핸들러 등록
@slack_app.message("야야")
def reply_yaya(message, say):
    user_id = message['user']
    say(f'뭐 <@{user_id}> 이 시키야')

@slack_app.message("환율")
def reply_exchange_rate(message, say):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_KEY}/latest/USD"
        response = requests.get(url)
        data = response.json()
        rate = data["conversion_rates"]["KRW"]
        rate = round(rate, 1)
        
        say(f'최근 업데이트된 원/달러 환율은 {rate}원입니다')
    except Exception as e:
        say(f'알 수 없는 오류로 환율을 파악할 수 없습니다.')

# 슬랙 챌린지 검증 (최초 Event API 등록 시 필요)
@app.post("/slack/message")
async def slack_challenge(request: Request):
    body = await request.json()
    if "challenge" in body:
        return JSONResponse(content={"challenge": body["challenge"]})
    return JSONResponse(content={})