# -*- coding: utf-8 -*-
import requests

black_urls = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS_mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_SS%2BAll_RUS.txt",
]

white_urls = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_universal.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-SNI-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
]

def preprocess_vpn_list(urls):
    raw_vpn_list = []
    for url in urls:
        r = requests.get(url.strip(), timeout=10)
        r.raise_for_status()
        vpn_urls = [line for line in r.text.split("\n") if not line.startswith("#") and line.strip()]
        raw_vpn_list.extend(vpn_urls)
    vpn_list = list(set(raw_vpn_list))
    print(str(len(vpn_list)) + "/" + str(len(raw_vpn_list)))
    return vpn_list

print("Processing black list...")
with open("black_list.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(preprocess_vpn_list(black_urls))))

print("Processing white list...")
with open("white_list.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(preprocess_vpn_list(white_urls))))

print("Done!")
