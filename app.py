import logging
import os
import secrets
from datetime import datetime
from textwrap import dedent

import dotenv
from flask import Flask, request, abort, render_template
from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction, LocationSendMessage, \
    BubbleContainer, FlexSendMessage, CarouselContainer
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from Members import members_blueprint
from database import MongoBuilder, MongoAdapter
from modules import COMMANDS, HELP_COMMANDS
from modules.sampledatasets import *

# preload required feature
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO, format='[FLASK] %(message)s')

# setting configuration
# configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.register_blueprint(members_blueprint, url_prefix='/members')
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))

# Configure Flask app logger
flask_logger = logging.getLogger('werkzeug')
flask_logger.setLevel(logging.INFO)

# global variable
OPENING_TIME = 9
CLOSING_TIME = 17  # 24:00 -> 24, 11:00 -> 11
db = MongoAdapter()


def mongo_build_operation():
    builder = MongoBuilder()
    name = "EmoCareCenter"
    collection = ["BodyHealth", "Exercise", "ObserveList", "Status"]
    builder.setup_database(database_name=name, collection_names=collection)
    builder.close_connection()
    caregivers = db.get_care_givers_data()
    db.insert_many("CareGivers", caregivers)
    db.insert_many("Profile", profile)
    db.insert_many("Status", status)
    db.insert_many("Exercise", exercise)
    db.insert_many("ObserveList", observe_list)
    db.insert_many("BodyHealth", body_health)
    # TODO 新增 caregivers 資料


def create_bubble_container(caregiver_data):
    return BubbleContainer(**caregiver_data)


def create_carousel_container(caregivers):
    bubbles = [create_bubble_container(caregiver) for caregiver in caregivers]
    return CarouselContainer(contents=bubbles)


@app.route("/")
def index():
    return render_template("index.html")


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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    line_user_id = event.source.user_id
    message_text = event.message.text
    found_key = None
    for key, value_list in COMMANDS.items():
        if message_text in value_list:
            found_key = key
            break

    if not found_key:
        message = "我看不懂這則訊息，但你可以按底下的按鈕選擇功能！\n\n"

        quick_reply_buttons = [
            QuickReplyButton(
                action=MessageAction(label=description[0], text=command)
            )
            for command, description in HELP_COMMANDS.items()
        ]

        # 使用 QuickReply 包装 QuickReplyButton 列表
        quick_reply = QuickReply(items=quick_reply_buttons)

        # 发送消息
        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=TextSendMessage(text=message, quick_reply=quick_reply)
        )
    else:
        if found_key == "回饋表單":
            message = TextSendMessage(
                text=dedent("""
                    (down)以下是回饋表單填寫處，點擊它(down)
                    https://forms.gle/kqcCTQvxJUEFPAuE8
                    
                    我們將會詳細的參考您給予的寶貴意見(!)
                    """).strip(),
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="給我們回饋", text="回饋")
                        )
                    ]
                )
            )

            line_bot_api.reply_message(
                reply_token=event.reply_token,
                messages=message
            )
        elif found_key == "top3":
            result = db.get_top_exercises()

            champion_name = result[0]["name"]
            second_name = result[1]["name"]
            third_name = result[2]["name"]
            champion_duration = result[0]["total_duration"]
            second_duration = result[1]["total_duration"]
            third_duration = result[2]["total_duration"]

            message = TextSendMessage(
                text=dedent(f"""
                        目前的運動健將 Top3 為：
                        第一名🥇：{champion_name} 
                            運動時數：{champion_duration} 🎉
                        第二名🥈：{second_name}
                            運動時數：{second_duration}
                        第三名🥉：{third_name}
                            運動時數：{third_duration}
                        """).strip()
            )
            line_bot_api.reply_message(
                reply_token=event.reply_token,
                messages=message
            )
        elif found_key == "照護人員":
            print(request.host)
            caregivers = db.get_care_givers_bubbles(domain=request.host)
            carousel_container = create_carousel_container(caregivers)
            flex_message = FlexSendMessage(alt_text="照護員", contents=carousel_container)

            # Create the additional text message with quick reply
            text_message = TextSendMessage(
                text="我們有這些照護人員喔 ⬆️😎⬆️",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="地址", text="地址在哪")
                        )
                    ]
                )
            )

            # Send both the flex message and the text message
            line_bot_api.reply_message(
                reply_token=event.reply_token,
                messages=[flex_message, text_message]
            )

        elif found_key == "預約時間":
            current_time = datetime.datetime.now()

            # Check if current time is after 5 PM
            if current_time.hour >= CLOSING_TIME:
                response_text = (
                    f"目前已超過客服時間（{CLOSING_TIME:02d}:00），請明天再進行預約。\n"
                    f"客服時間為每日 {OPENING_TIME:02d}:00 - {CLOSING_TIME:02d}:00，感謝您的理解。"
                )
                line_bot_api.reply_message(
                    reply_token=event.reply_token,
                    messages=TextSendMessage(text=response_text)
                )
            else:
                response_text = (
                    f"您好！正在為您安排服務請稍後喔~\n"
                    f"（客服時間只到 {CLOSING_TIME:02d}:00，如超過時間沒回應請見諒。）"
                )
                reserve_form_text = (
                    dedent("""
                        好的!
                        (down)請到下方連結的表單進行預約(down)
                        https://forms.gle/LtzYTFfWW8LyiGRz8
                        """).strip()
                )
                line_bot_api.reply_message(
                    reply_token=event.reply_token,
                    messages=[
                        TextSendMessage(text=response_text),
                        TextSendMessage(text=reserve_form_text)
                    ]
                )
        elif found_key == "客服":
            current_time = datetime.datetime.now()

            # Check if current time is after 5 PM
            if current_time.hour >= CLOSING_TIME:
                response_text = (
                    f"目前已超過客服時間（{CLOSING_TIME:02d}:00），請明天再進行預約。\n"
                    f"客服時間為每日 {OPENING_TIME:02d}:00 ~ {CLOSING_TIME:02d}:00，感謝您的理解。"
                )
                line_bot_api.reply_message(
                    reply_token=event.reply_token,
                    messages=TextSendMessage(text=response_text)
                )
            else:
                response_text = (
                    f"您好！正在為您安排服務請稍後喔~\n"
                    f"（客服時間只到 {CLOSING_TIME:02d}:00，如超過時間沒回應請見諒。）"
                )
                reserve_form_text = (
                    dedent("""
                        好的!
                        (down)請到下方連結的表單進行預約(down)
                        https://forms.gle/LtzYTFfWW8LyiGRz8
                        """).strip()
                )
                line_bot_api.reply_message(
                    reply_token=event.reply_token,
                    messages=[
                        TextSendMessage(text=response_text),
                        TextSendMessage(text=reserve_form_text)
                    ]
                )
        elif found_key == "地址":
            location = LocationSendMessage(title='位置資訊',
                                           address='912屏東縣內埔鄉學府路1號',
                                           latitude=22.6408666,
                                           longitude=120.5951299)
            message = TextSendMessage(
                text="本日照中心地址位於："
            )
            line_bot_api.reply_message(
                reply_token=event.reply_token,
                messages=[message, location]
            )
        elif found_key == "營業時間":
            message = TextSendMessage(
                text=dedent(
                    f"""
                    日照中心的營業時間為：
                    星期一 {OPENING_TIME:02d}:00 ~ {CLOSING_TIME:02d}:00
                    星期二 {OPENING_TIME:02d}:00 ~ {CLOSING_TIME:02d}:00
                    星期三 {OPENING_TIME:02d}:00 ~ {CLOSING_TIME:02d}:00
                    星期四 {OPENING_TIME:02d}:00 ~ {CLOSING_TIME:02d}:00
                    星期五 {OPENING_TIME:02d}:00 ~ {CLOSING_TIME:02d}:00
                    星期六 休息日(!)
                    星期日 休息日(!)
                    """).strip()
            )
            line_bot_api.reply_message(
                reply_token=event.reply_token,
                messages=message
            )
        elif found_key == "運動查詢":
            url = request.host_url.rstrip('/')  # 移除末尾的斜杠
            message = TextSendMessage(
                text=dedent(
                    f"""
                    👇 登入網站查詢 👇
{url}/members/main
                    """.strip()
                )
            )
            line_bot_api.reply_message(
                reply_token=event.reply_token,
                messages=message
            )
        elif found_key == "你好":
            message = TextSendMessage(
                text="請問需要甚麼服務嗎？",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="照護人員", text="照護人員")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="營業時間", text="營業時間")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="地點", text="地址在哪")
                        )
                    ]
                )
            )
            line_bot_api.reply_message(
                reply_token=event.reply_token,
                messages=message
            )


if __name__ == "__main__":
    mongo_build_operation()
    app.run(host='0.0.0.0', port=5000, debug=True)
