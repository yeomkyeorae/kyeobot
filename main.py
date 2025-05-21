from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

f = open("./slack.key")
lines = f.readlines()
slack_bot_token = lines[0].strip()
slack_app_token = lines[1].strip()
f.close()

# Initializes your app with your bot token and socket mode handler
app = App(token=slack_bot_token)

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, slack_app_token).start()