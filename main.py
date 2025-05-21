from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler

f = open("./slack.key")
lines = f.readlines()
SLACK_BOT_TOKEN = lines[0].strip()
SLACK_SIGNING_SECRET = lines[1].strip()
SLACK_APP_LEVEL = lines[2].strip()
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

# 슬랙 챌린지 검증 (최초 Event API 등록 시 필요)
@app.post("/slack/message")
async def slack_challenge(request: Request):
    body = await request.json()
    if "challenge" in body:
        return JSONResponse(content={"challenge": body["challenge"]})
    return JSONResponse(content={})