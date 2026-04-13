import os
import requests
import json
from datetime import datetime

# 1. 금고에서 열쇠 꺼내기
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
API_KEY = os.environ.get('API_KEY')

# 2. 뉴스 통합 브리핑 프롬프트
today_date = datetime.now().strftime('%Y년 %m월 %d일')
prompt = f"""
오늘은 {today_date}야. 
대한민국 주요 언론사의 실시간 헤드라인과 주요 이슈를 확인해서 
아래 카테고리별로 가장 중요한 뉴스 3~5개를 통합해서 브리핑해 줘.

[브리핑 포함 내용]
1. 정치/경제: 오늘 가장 뜨거운 정책이나 시장 변화
2. 사회/국제: 꼭 알아야 할 주요 사건 및 사고
3. IT/테크: 신기술, 출시 소식 또는 업계 동향
4. 한 줄 요약: 오늘 아침 가장 핵심적인 한 문장

[작성 규칙]
- 말투는 간결하고 신뢰감 있는 뉴스 브리핑 톤으로.
- 가독성이 좋게 이모지를 적절히 사용해 줘.
"""

# 3. 제미나이 호출 (🚨 2.5 최신 버전으로 수정 완료!)
print("실시간 뉴스를 통합 분석 중입니다...")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}
data = {
    "contents": [{
        "parts": [{"text": prompt}]
    }]
}

response = requests.post(url, headers=headers, data=json.dumps(data))
result = response.json()

# 4. 결과 정리
if 'candidates' in result:
    news_content = result['candidates'][0]['content']['parts'][0]['text']
    news_content = news_content.replace('*', '') 
    final_message = "📢 [" + today_date + "] 대한민국 통합 뉴스 브리핑\n\n" + news_content
else:
    final_message = "🚨 제미나이 에러 상세내용: " + str(result)

# 5. 텔레그램 발송
def send_telegram_message(token, chat_id, text):
    telegram_url = "https://api.telegram.org/bot" + str(token) + "/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(telegram_url, json=payload)

print("텔레그램으로 브리핑을 전송합니다...")
send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, final_message)
print("전송 완료!")
