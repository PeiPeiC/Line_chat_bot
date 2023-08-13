from django.shortcuts import render
from django.http import HttpResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from django.views.decorators.csrf import csrf_exempt
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# Retrieve the values from the .env file
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

LINE_BOT_API = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
HANDLER = WebhookHandler(LINE_CHANNEL_SECRET)
# Constant
RANKINGS_DIR = os.path.join(os.path.dirname(__file__), 'rankings')
USER_STATES = {}


@csrf_exempt  # Add this decorator to bypass CSRF verification for Line webhook
def line_webhook(request):
    if request.method == 'POST':
        signature = request.headers['X-Line-Signature']
        body = request.body.decode()
        try:
            HANDLER.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)
        return HttpResponse(status=200)
    return HttpResponse(status=405)


def load_ranking_data():
    sources = ["ARWU", "QS", "THE"]
    all_data = []
    for source in sources:
        file_path = os.path.join(RANKINGS_DIR, f"{source}_rankings.json")
        with open(file_path, encoding='utf-8') as file:
            all_data.extend(json.load(file))
    return all_data


RANKINGS_DATA = load_ranking_data()


def search_university_rankings(keyword):
    keyword_lower = keyword.lower()
    return [entry for entry in RANKINGS_DATA if keyword_lower in entry['University'].lower()]


def get_university_ranking(user_message):
    search_results = search_university_rankings(user_message)

    if search_results:
        universities = {}
        for result in search_results:
            university_name = result['University']
            ranking = result['Ranking']
            source = result['Source']
            year = result['Year']

            key = university_name
            if key in universities:
                existing_ranking = universities[key]
                for i, (existing_year, existing_source, existing_rank) in enumerate(existing_ranking):
                    if existing_year == year and existing_source == source:
                        if ranking.isdigit() and (existing_rank == '' or not existing_rank.isdigit() or int(ranking) > int(existing_rank)):
                            existing_ranking[i] = (year, source, ranking)
                        break
                else:
                    existing_ranking.append((year, source, ranking))
            else:
                universities[key] = [(year, source, ranking)]

        reply_text = ""
        for university_name, rankings in universities.items():
            # Sort by year in descending order
            sorted_rankings = sorted(
                rankings, key=lambda x: x[0], reverse=True)
            reply_text += f"{university_name}\n"
            for year, source, ranking in sorted_rankings:
                reply_text += f"{year} {source}: {ranking}\n"
            reply_text += "\n"
    else:
        reply_text = "No rankings found for the given university."
    return reply_text


def handle_school_list_query():
    reply_text = "Computer Science Conversion Programmes List\n"
    reply_text += "https://www.cs-conversion-list.com/"
    return TextSendMessage(text=reply_text)


def handle_study_forum_query():
    reply_message = TemplateSendMessage(
        alt_text="留學論壇",
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title="英語系論壇",
                    text="可以到各校校版查詢申請進度",
                    actions=[
                        URIAction(label="The Student Room",
                                  uri="https://www.thestudentroom.co.uk/"),
                        URIAction(label="Reddit",
                                  uri="https://www.reddit.com/?feed=home")
                    ]
                ),
                CarouselColumn(
                    title="大陸論壇",
                    text="可查詢#轉碼申請#轉碼項目推薦",
                    actions=[
                        URIAction(label="一畝三分地",
                                  uri="https://www.1point3acres.com/bbs/"),
                        URIAction(
                            label="小紅書", uri="https://www.xiaohongshu.com/search_result?keyword=%25E8%25BD%25AC%25E7%25A0%2581%25E7%2595%2599%25E5%25AD%25A6&source=web_search_result_notes"),

                    ]
                ),
                CarouselColumn(
                    title="台灣論壇",
                    text="PTT另有英國留學版、荷蘭留學版、雅思版",
                    actions=[
                        URIAction(
                            label="PTT 留學版", uri="https://www.pttweb.cc/bbs/studyabroad"),
                        URIAction(label="Dcard 留學版",
                                  uri="https://www.dcard.tw/f/studyabroad"),
                    ]
                ),
            ]
        )
    )
    return reply_message


def handle_scholarship_info_query():
    reply_text = "獎學金資訊:\n"
    reply_text = "獎學金資訊:\n"
    reply_text += "1. 學校自行提供校內獎學金: 至各校網站查詢 Scholarship and Funding\n"
    reply_text += "2. 英國文化協會 IELTS Prize 雅思獎金(限在 British Council 考雅思的人申請): https://tw.ieltsasia.org/IELTS%E7%8D%8E%E9%87%91\n"
    reply_text += "3. 留學代辦提供的獎學金:\n"
    reply_text += "- IDP\n"
    reply_text += "- Intake Impact Scholarship (限透過 Intake 遞交申請的學生): https://intake.education/tw/intake-impact-scholarship\n"
    reply_text += "4. Chevening Scholarships (注意有返台義務不能申請 PSW): https://www.chevening.org/scholarships/\n"
    reply_text += "5. Scottish Power 限特定校系: https://www.scottishpower.com/pages/scottishpower_masters_scholarships.aspx\n"
    reply_text += "6. 歐洲留學獎學金: https://eef-taiwan.org.tw/study_in_europe/scholarship/european_scholarship\n"
    reply_text += "7. 其他獎學金查詢平台:\n"
    reply_text += "- International Scholarships Search: https://www.internationalscholarships.com/\n"
    reply_text += "- International Students: https://www.internationalstudent.com/scholarships/\n"
    reply_text += "- scholars4dev: https://www.scholars4dev.com/category/scholarships-list/\n"
    reply_text += "- Scholarship Portal: https://www.scholarshipportal.com/\n"
    reply_text += "- Postgraduate Studentships(UK): https://www.postgraduatestudentships.co.uk/\n"
    return TextSendMessage(text=reply_text)


# ... [Handle each special query and return the appropriate reply text]
# Use a dictionary to map the user message to the appropriate handler function:
SPECIAL_QUERY_HANDLERS = {
    "學校清單": handle_school_list_query,
    "留學論壇": handle_study_forum_query,
    "獎學金資訊": handle_scholarship_info_query,
}


def handle_special_queries(user_message):
    handler = SPECIAL_QUERY_HANDLERS.get(user_message)
    if handler:
        return handler()

    # If no specific handler is found, return the default message.
    return default_reply_message()


def default_reply_message():
    # ... [Return the default carousel message]
    reply_message = TemplateSendMessage(
        alt_text="功能說明",
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title="選校",
                    text="選校",
                    actions=[
                        MessageAction(label="學校清單", text="學校清單"),
                        MessageAction(label="查詢學校排名", text="查詢學校排名")
                    ]
                ),
                CarouselColumn(
                    title="留學資源查詢",
                    text="點擊以查詢留學資源",
                    actions=[
                        MessageAction(label="留學論壇", text="留學論壇"),
                        MessageAction(label="獎學金資訊", text="獎學金資訊")
                    ]
                ),
            ]
        )
    )
    return reply_message


@HANDLER.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    # Check if user_id exists in USER_STATES, otherwise initialize it
    if user_id not in USER_STATES:
        USER_STATES[user_id] = {
            "waiting_for_university_name": False, "count": 0}

    # Set a default reply_message here
    reply_message = default_reply_message()

    if "查詢學校排名" in user_message:
        USER_STATES[user_id]["waiting_for_university_name"] = True
        USER_STATES[user_id]["count"] = 0
        reply_message = TextSendMessage(
            text="請輸入學校名稱(英文全名為佳)\n 可連續搜尋10次，離開請輸入0或Exit")

    elif USER_STATES[user_id]["waiting_for_university_name"]:
        USER_STATES[user_id]["count"] += 1
        reply_text = get_university_ranking(user_message)
        print("enter get uni ranking")
        if user_message in ['Exit', '0'] or USER_STATES[user_id]["count"] >= 10:
            USER_STATES[user_id]["waiting_for_university_name"] = False
            USER_STATES[user_id]["count"] = 0
            reply_text = "查詢結束，希望有幫助到您，欲重新查詢請重新輸入 : 查詢學校排名 "
        reply_message = TextSendMessage(text=reply_text)

    else:
        reply_message = handle_special_queries(user_message)

    print("Reply Message:", reply_message)
    LINE_BOT_API.reply_message(event.reply_token, reply_message)
