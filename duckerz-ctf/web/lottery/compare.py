import requests
import hashlib

url_base = 'http://94.19.79.169:20001/api'


def get_ticket_for_user(username, password):
    """Получаем билет для конкретного пользователя"""

    # Регистрация
    requests.post(f'{url_base}/auth/register',
                  json={'username': username, 'password': password})

    # Логин
    response = requests.post(f'{url_base}/auth/login',
                             json={'username': username, 'password': password})

    cookies = response.cookies

    # Получаем билет
    response = requests.post(f'{url_base}/ticket/get', cookies=cookies)
    ticket = response.json().get('ticket', 'unknown')

    return ticket


# Тест 1: Один и тот же пользователь всегда получает один билет?
print("[*] Test 1: Same user, same ticket?")
username = 'test_same_user'
password = 'pass123'

ticket1 = get_ticket_for_user(username, password)
print(f"First login: {ticket1}")

# Логинимся ещё раз
response = requests.post(f'{url_base}/auth/login',
                         json={'username': username, 'password': password})
cookies = response.cookies
response = requests.post(f'{url_base}/ticket/get', cookies=cookies)
ticket2 = response.json().get('ticket', 'unknown')
print(f"Second login: {ticket2}")
print(f"Same ticket: {ticket1 == ticket2}\n")

# Тест 2: Билет зависит от имени пользователя?
print("[*] Test 2: Ticket based on username?")
for i in range(5):
    username = f'test_user_{i}'
    ticket = get_ticket_for_user(username, f'pass{i}')

    # Проверим разные хэши
    md5_user = hashlib.md5(username.encode()).hexdigest()[:8]

    print(f"{username}: {ticket}")
    print(f"  MD5(username)[:8]: {md5_user}")
    print(f"  Match: {md5_user in ticket}")
    print()

# Тест 3: Может билет основан на JSESSIONID?
print("[*] Test 3: Multiple logins for same user")
username = 'test_session'
password = 'pass123'

tickets = []
for i in range(3):
    ticket = get_ticket_for_user(username, password)
    tickets.append(ticket)
    print(f"Attempt {i + 1}: {ticket}")

print(f"All same: {len(set(tickets)) == 1}")