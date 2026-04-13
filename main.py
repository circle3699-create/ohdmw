import os
import requests
import json
from datetime import datetime

# 1. 깃허브 금고(Secrets)에서 정보 가져오기
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
API_KEY = os.environ.get('API_KEY')

today_date = datetime.now().strftime('%Y년 %m월 %d일')

def ask_gemini_pro(system_role, task_instruction, context_data=""):
    """Gemini 1.5 Pro 모델을 호출하는 고성능 엔진"""
    # 유료 티어의 성능을 십분 발휘하기 위해 gemini-1.5-pro 모델을 명시합니다.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    # 에이전트의 전문성을 극대화하는 프롬프트 구조
    full_prompt = f"""
    당신은 전 세계 최고의 전문가 그룹의 일원인 '{system_role}'입니다.
    
    [참조 데이터]
    {context_data if context_data else '최신 글로벌 트렌드 데이터베이스'}
    
    [수행 과업]
    {task_instruction}
    
    [작성 가이드]
    - 상장사 대표에게 직접 보고하는 수준의 전문적이고 냉철한 톤을 유지하세요.
    - 단순 나열이 아닌, 데이터 간의 상관관계와 비즈니스 기회를 통찰력 있게 분석하세요.
    """
    
    data = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "temperature": 0.7,  # 창의성과 논리성의 균형
            "topP": 0.95,
            "maxOutputTokens": 4096
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    res_json = response.json()
    
    if 'candidates' in res_json:
        return res_json['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"에러 발생: {res_json}"

# --- [에이전트 팀 프로젝트 가동] ---

print(f"[{today_date}] Gemini 1.5 Pro 팀 프로젝트를 시작합니다...")

# Step 1: 글로벌 R&D 분석 (리서처)
print("1단계: 기술 리서처가 글로벌 특허 및 성분 혁신사례를 정밀 분석 중...")
research_task = "글로벌 화장품 시장에서 '초고효능(High-Performance)'을 구현하는 최신 성분 특허 2가지와 원료사 동향을 분석해줘."
research_result = ask_gemini_pro("글로벌 뷰티 테크 R&D 분석가", research_task)

# Step 2: 타겟 맞춤 제품 기획 (상품 BM)
print("2단계: 수석 BM이 피트니스/피부 장벽 특화 제품을 설계 중...")
planning_task = "위 리서치 결과를 바탕으로, '운동 전후 피부 관리'에 특화된 고기능성 스킨케어 제품을 기획해줘. 타겟은 구매력이 높은 3040 오피니언 리더층이야."
planning_result = ask_gemini_pro("K-뷰티 럭셔리 브랜드 수석 기획자", planning_task, research_result)

# Step 3: 수익성 및 전략 검토 (디렉터)
print("3단계: 전략 디렉터가 최종 보고서를 완성 중...")
final_task = "기획안의 시장 진입 장벽(MOAT)과 마케팅 핵심 전략을 수립하고, 대표님이 즉시 승인할 수 있는 최종 의사결정 리포트로 요약해줘."
final_report = ask_gemini_pro("상장사 엑시트 경험의 비즈니스 전략가", final_task, planning_result)

# --- [텔레그램 최종 전송] ---

final_message = f"🏆 [Gemini Pro 전략 리포트] {today_date}\n\n{final_report.replace('*', '')}"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    # 메시지가 길 수 있으므로 분할 전송 처리는 생략하고 4096자 내외로 전송
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

send_telegram(final_message)
print("전략 보고서 전송 완료!")
