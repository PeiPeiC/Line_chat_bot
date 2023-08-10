from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from django.views.decorators.csrf import csrf_exempt

import json
import os

line_bot_api = LineBotApi('CQm0BL4z/a2K/U83zm7QbTMWGBkmjlUXvurjeYQxHXNKZy5uUmpcUzaV+xY1oM/JbDxttHOkIWtSfCucgDvtRiiSCq1p6fmx7neitBe3GZ5B11Fq8IHyUGRB2o/w3b7U4TP7miGzB9ibjyKuQhx59AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ba98c88fab9fdec489f9b5bb31e53fe0')

@csrf_exempt  # Add this decorator to bypass CSRF verification for Line webhook
def line_webhook(request):
    if request.method == 'POST':
        signature = request.headers['X-Line-Signature']
        body = request.body.decode()
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)
        return HttpResponse(status=200)
    return HttpResponse(status=405)


# Use the relative path to the 'rankings' directory
RANKINGS_DIR = os.path.join(os.path.dirname(__file__), 'rankings')

def load_ranking_data(source):
    file_path = os.path.join(RANKINGS_DIR, f"{source}_rankings.json")
    with open(file_path, encoding='utf-8') as file:
        return json.load(file)

def search_university_rankings(keyword):
    all_data = []
    sources = ["ARWU", "QS", "THE"]
    
    for source in sources:
        data = load_ranking_data(source)
        all_data.extend(data)

    keyword_lower = keyword.lower()
    results = [entry for entry in all_data if keyword_lower in entry['University'].lower()]
    print("Search results:", results)  # Add this line for logging
    return results

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
            sorted_rankings = sorted(rankings, key=lambda x: x[0], reverse=True)  # Sort by year in descending order
            reply_text += f"{university_name}\n"
            for year, source, ranking in sorted_rankings:
                reply_text += f"{year} {source}: {ranking}\n"
            reply_text += "\n"
    else:
        reply_text = "No rankings found for the given university."

    return reply_text

# Add a global variable to keep track of the state
waiting_for_university_name = False
count = 0
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    global waiting_for_university_name
    user_message = event.message.text

    if user_message == "學校清單":
        reply_text = "Computer Science Conversion Programmes List\n"
        reply_text += "https://www.cs-conversion-list.com/"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    elif user_message == "留學論壇":
        reply_message = TemplateSendMessage(
            alt_text="留學論壇",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title="英語系論壇",
                        text="可以到各校校版查詢申請進度",
                        actions=[
                            URIAction(label="The Student Room", uri="https://www.thestudentroom.co.uk/"),
                            URIAction(label="Reddit", uri="https://www.reddit.com/?feed=home")                           
                        ]
                    ),
                    CarouselColumn(
                        title="大陸論壇",
                        text="可查詢#轉碼申請#轉碼項目推薦",
                        actions=[
                            URIAction(label="一畝三分地", uri="https://www.1point3acres.com/bbs/"),
                            URIAction(label="小紅書", uri="https://www.xiaohongshu.com/search_result?keyword=%25E8%25BD%25AC%25E7%25A0%2581%25E7%2595%2599%25E5%25AD%25A6&source=web_search_result_notes"),
                            
                        ]
                    ),
                    CarouselColumn(
                        title="台灣論壇",
                        text="PTT另有英國留學版、荷蘭留學版、雅思版",
                        actions=[
                            URIAction(label="PTT 留學版", uri="https://www.pttweb.cc/bbs/studyabroad"),
                            URIAction(label="Dcard 留學版", uri="https://www.dcard.tw/f/studyabroad"),
                        ]
                    ),            
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            reply_message
        )



    elif user_message == "獎學金資訊":
            reply_text = "獎學金資訊:\n"
            reply_text += "1. 學校自行提供校內獎學金: 至各校網站查詢 Scholarship and Funding\n"
            reply_text += "2. 英國文化協會 IELTS Prize 雅思獎金(限在 British Council 考雅思的人申請): https://tw.ieltsasia.org/IELTS%E7%8D%8E%E9%87%91\n"
            reply_text += "3. 留學代辦提供的獎學金:\n"
            reply_text += "- IDP\n"
            reply_text += "- Intake Impact Scholarship (限透過 Intake 遞交申請的學生): https://intake.education/tw/intake-impact-scholarship\n"
            reply_text += "4. Chevening Scholarships (注意有返台義務不能申請 PSW): https://www.chevening.org/scholarships/\n"
            reply_text += "5. Scottish Power 限特定校系: https://www.scottishpower.com/pages/scottishpower_masters_scholarships.aspx\n"
            reply_text += "6. 其他獎學金查詢平台:\n"
            reply_text += "- International Scholarships Search: https://www.internationalscholarships.com/\n"
            reply_text += "- International Students: https://www.internationalstudent.com/scholarships/\n"
            reply_text += "- scholars4dev: https://www.scholars4dev.com/category/scholarships-list/\n"
            reply_text += "- Scholarship Portal: https://www.scholarshipportal.com/\n"
            reply_text += "- Postgraduate Studentships(UK): https://www.postgraduatestudentships.co.uk/\n"

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
    elif "查詢學校排名" in user_message:
        waiting_for_university_name = True  # Set the state to True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入學校名稱(英文全名為佳)\n 可繼續搜尋10次，離開請輸入0或stop")
        )

    elif waiting_for_university_name:
        count += 1
        # Now the user has entered the university name after receiving the "請輸入學校名稱(全名)" message
        # Get the university ranking information
        print("Received university name:", user_message)  # Add this line for logging
        reply_text = get_university_ranking(user_message)
        print("Reply text:", reply_text)  # Add this line for logging

        # Send the ranking information back to the user
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
        
        if user_message == 'stop' or user_message == '0' or count >=10 :
            waiting_for_university_name = False
            count = 0
            # Reset the state after handling the input
            


    else:
        # Handle other cases with a carousel template
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

        line_bot_api.reply_message(
            event.reply_token,
            reply_message
        )
