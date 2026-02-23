import requests

url_base = 'http://94.19.79.169:20001/api'

# Проверяем одного из "победителей"
username = 'user_6386'
password = 'pass123'

# Логин
response = requests.post(f'{url_base}/auth/login',
                        json={'username': username, 'password': password})

print(f"Login status: {response.status_code}")
print(f"Login response: {response.json()}\n")

cookies = response.cookies

# Получаем билет
response = requests.post(f'{url_base}/ticket/get', cookies=cookies)
print(f"Get ticket status: {response.status_code}")
print(f"Get ticket response: {response.json()}\n")

# Проверяем
response = requests.post(f'{url_base}/ticket/check', cookies=cookies)
print(f"Check status: {response.status_code}")
print(f"Check response: {response.json()}\n")

# Выведем полный текст ответа
print(f"Full response text: {response.text}")