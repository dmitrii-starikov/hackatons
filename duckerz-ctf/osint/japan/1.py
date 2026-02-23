import requests
import math
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===== НАСТРОЙКИ =====
CENTER_LAT = 26.5946746258
CENTER_LON = 127.9717634260

STEP_METERS = 20
RADIUS_METERS = 1500

MAX_WORKERS = 10   # количество потоков (10–20)
TIMEOUT = 5

URL = "https://maps.duckerz.ru:50012/submit"

BAD_RESPONSE = {"not": "aaa"}

HEADERS = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Origin": "https://maps.duckerz.ru:50012",
    "Referer": "https://maps.duckerz.ru:50012/?",
}

# ====================

stop_event = threading.Event()
session = requests.Session()


def meters_to_lat(m):
    return m / 111000.0


def meters_to_lon(m, lat):
    return m / (111000.0 * math.cos(math.radians(lat)))


def generate_points(lat, lon, radius, step):
    lat_step = meters_to_lat(step)
    lon_step = meters_to_lon(step, lat)
    max_offset = int(radius / step)

    for i in range(-max_offset, max_offset + 1):
        for j in range(-max_offset, max_offset + 1):
            if math.hypot(i * step, j * step) > radius:
                continue
            yield (
                lat + i * lat_step,
                lon + j * lon_step
            )


def submit_point(lat, lon):
    if stop_event.is_set():
        return None

    payload = {"lat": f"{lat}", "lon": f"{lon}"}

    try:
        r = session.post(URL, json=payload, headers=HEADERS, timeout=TIMEOUT)
        try:
            resp = r.json()
        except Exception:
            resp = {"_raw": r.text}

    except Exception as e:
        return None

    if resp != BAD_RESPONSE:
        stop_event.set()
        print("\n🎯 FOUND!")
        print("LAT:", lat)
        print("LON:", lon)
        print("RESPONSE:", json.dumps(resp, indent=2))
        sys.exit(0)

    return None


def main():
    points = list(generate_points(CENTER_LAT, CENTER_LON, RADIUS_METERS, STEP_METERS))
    print(f"[+] Generated {len(points)} points")
    print(f"[+] Using {MAX_WORKERS} threads\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(submit_point, lat, lon) for lat, lon in points]

        for _ in as_completed(futures):
            if stop_event.is_set():
                break

    print("[-] Nothing found in this area")


if __name__ == "__main__":
    main()
