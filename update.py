import requests
from concurrent.futures import ThreadPoolExecutor
import geoip2.database
import socket
import re

READER = geoip2.database.Reader('GeoLite2-Country.mmdb')

black_urls = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS_mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_SS%2BAll_RUS.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/V2Ray-Config-By-EbraSha.txt",
]

white_urls = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_universal.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-SNI-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
]

def get_country(host):
    try:
        ip = host if host.replace('.', '').isdigit() else socket.gethostbyname(host)
        r = READER.country(ip)

        flag = ''.join(chr(127397 + ord(c)) for c in r.country.iso_code)
        return f"{flag} | {r.country.name}"
    except: return None

def write_as_country(line: str):
    match = re.match(r'(.*?://[^@]+@)([^#]+)(#)(.+)', line)
    if not match: return None
    info = get_country(match.group(2).split(":")[0])
    return f"{match.group(1)}{match.group(2)}#{info}".replace('?#', '#') if info else None

def fetch(url: str):
    try: return [l for l in requests.get(url, timeout=10).text.splitlines() if l and not l.startswith("#")]
    except: return []

def preprocess_vpn_list(urls: list):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch, urls))
    raw_list = [item for sublist in results for item in sublist]
    return sorted(set(raw_list))

# Сохроанение в файлы
with open("black_list.txt", "w", encoding="utf-8") as f:
    vpn_list = sorted(filter(None, map(write_as_country, preprocess_vpn_list(black_urls))))
    f.write("\n".join(vpn_list))

with open("white_list.txt", "w", encoding="utf-8") as f:
    vpn_list = preprocess_vpn_list(white_urls)
    f.write("\n".join(vpn_list))
