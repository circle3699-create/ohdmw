import os
import requests
import json
from datetime import datetime

# 1. 환경 설정
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
API_KEY = os.environ.get('API_KEY')

# 2. 에이전트 팀 협업 프롬프트
today_date = datetime.now().strftime('%Y년 %m월 %d일')
team_prompt = f"""
너는 이제부터 1인 기업 대표님을 보좌하는 'AI 화장품 런칭 팀'이야. 
아래 세 명의 전문가가 순차적으로 협업하여 오늘 아침 최종 보고서를 작성해.

---
[단계 1: R&D 리서처의 기술 조사]
전 세계 최신 화장품 특허와 신성분 소식을 분석해. 
특히 기존 성분의 한계를 극복한 신기술(예: 흡수율 개선, 천연 대체 성분 등)을 3가지 선정해.

[단계 2: BM 기획자의 제품 설계]
리서처가 뽑은 성분 중 가장 시장성이 높은 하나를 골라 제품을 기획해.
- 제품명(가제), 타겟 고객, 핵심 소구점(USP), 예상 원가 구조 분석을 포함해.

[단계 3: 전략 디렉터의 최종 검수 및 보고]
상장사 대표의 시각에서 위 기획안의 리스크를 점검하고, 
'수익성'과 '차별화' 관점에서 최종 수정 제안을 더해 텔레그램 보고용으로 요약해.
---

오늘 날짜: {today_date}
모든 과정은 논리적이고 전문적이어야 하며, 대표님이 즉시 의사결정할 수 있는 수준으로 작성해.
"""

# 3. AI 실행 (Gemini 2.5 Flash 혹은 1.5 사용)
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}
data = {"contents": [{"parts": [{"text": team_prompt}]}]}

print("AI 에이전트 팀이 회의를 시작합니다...")
response = requests.post(url, headers=headers, data=json.dumps(data))
result = response.json()

# 4. 결과 정리 및 전송
if 'candidates' in result:
    final_report = result['candidates'][0]['content']['parts'][0]['text'].replace('*', '')
    message = f"🚀 [AI 팀 협업 보고] {today_date}\n\n{final_report}"
else:
    message = f"🚨 팀 회의 중 오류 발생: {result}"

def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

send_telegram(TELEGRAM_TOKEN, CHAT_ID, message)
print("대표님께 보고서 전송을 마쳤습니다.")
