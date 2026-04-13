import os
import requests
import json
from datetime import datetime

# 1. 환경 변수에서 정보 가져오기
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
API_KEY = os.environ.get('API_KEY')

# 2. 뉴스 통합 브리핑 프롬프트
# 제미나이에게 한국 주요 언론사의 뉴스를 검색하고 요약하도록 지시합니다.
today_date = datetime.now().strftime('%Y년 %m월 %d일')
prompt = f"""
오늘은 {today_date}야. 
대한민국 주요 언론사(네이버 뉴스, 다음 뉴스, 주요 일간지 등)의 실시간 헤드라인과 주요 이슈를 확인해서 
아래 카테고리별로 가장 중요한 뉴스 3~5개를 통합해서 브리핑해 줘.

[브리핑 포함 내용]
1. 정치/경제: 오늘 가장 뜨거운 정책이나 시장 변화
2. 사회/국제: 꼭 알아야 할 주요 사건 및 사고
3. IT/테크: 신기술, 출시 소식 또는 업계 동향
4. 한 줄 요약: 오늘 아침 가장 핵심적인 한 문장

[작성 규칙]
- 말투는 간결하고 신뢰감 있는 뉴스 브리핑 톤으로 작성해 줘.
- 각 뉴스에는 짧은 요약과 가능하면 관련 키워드를 포함해 줘.
- 가독성이 좋게 이모지를 적절히 사용해 줘.
"""

# 3. 제미나이(Gemini 1.5 Flash) 호출
print("실시간 뉴스를 통합 분석 중입니다...")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}
data = {
    "contents": [{
        "parts": [{"text": prompt}]
    }]
}

response = requests.post(url, headers=headers, data=json.dumps(data))
result = response.json()

# 4. 결과 정리 및 메시지 생성
if 'candidates' in result:
    news_content = result['candidates'][0]['content']['parts'][0]['text']
    news_content = news_content.replace('*', '') # 가독성을 위해 특수문자 제거
    final_message = f"📢 [{today_date}]
