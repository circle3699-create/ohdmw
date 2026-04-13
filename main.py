import requests
import os

# 환경 변수에서 API 키와 텔레그램 토큰 가져오기
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
YOUR_CHAT_ID = 'YOUR_CHAT_ID'  # 텔레그램 사용자 ID 또는 그룹 ID 입력

def fetch_news():
    # Gemini API와 통신하여 뉴스 가져오기
    url = 'https://api.geminisite.com/v1/news'
    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles
    else:
        print("Error fetching news:", response.status_code)
        return []

def send_to_telegram(message):
    telegram_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': YOUR_CHAT_ID,
        'text': message,
    }
    response = requests.post(telegram_url, data=payload)
    return response

def main():
    articles = fetch_news()
    if articles:
        for article in articles:
            title = article['title']
            url = article['url']
            message = f"{title}: {url}"
            send_to_telegram(message)

if __name__ == '__main__':
    main()
