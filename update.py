# -*- coding: utf-8 -*-
import requests
from concurrent.futures import ThreadPoolExecutor

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

def fetch(url):
    try:
        return [l for l in requests.get(url, timeout=10).text.splitlines() if l and not l.startswith("#")]
    except: return []

def preprocess_vpn_list(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch, urls))
    
    raw_list = [item for sublist in results for item in sublist]
    return sorted(set(raw_list))


with open("black_list.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(preprocess_vpn_list(black_urls))))

with open("white_list.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(preprocess_vpn_list(white_urls))))

