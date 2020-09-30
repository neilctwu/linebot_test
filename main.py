from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
flag = True
activate_ = False

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global flag
    global activate_

    if event.message.text == '啟動地鼠':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='我是  做了32年臨櫃 林桂翔'))
        activate_ = True

    if event.message.text == '地鼠88':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='運動中心老師 有個淺規則 不能跟學員亂來'))
        activate_ = False
        return

    if activate_:
        if flag:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='建議'))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='運動'))
        flag = not flag


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)