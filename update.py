import requests
from concurrent.futures import ThreadPoolExecutor
import socket
import ssl

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

def is_alive(line):
    try:
        if "://" in line:
            part = line.split('@')[1].split('#')[0]
            host_port, params_str = part.split('?')[0], part.split('?')[1] if '?' in part else ''
            host, port = host_port.rsplit(':', 1)
            is_tls = "security=tls" in params_str or "security=reality" in params_str or "publicKey=" in params_str
            sni = host
            if "sni=" in params_str: sni = params_str.split('sni=')[1].split('&')[0]
        else:
            if ':' not in line: return True
            host, port = line.split('/')[0].rsplit(':', 1)
            is_tls, sni = False, None

        s = socket.socket(); s.settimeout(2)
        s.connect((host, int(port)))
        
        if is_tls:
            ctx = ssl.create_default_context()
            ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
            s = ctx.wrap_socket(s, server_hostname=sni)
            s.close()
            return True
        else:
            s.close()
            return True
    except: return False

def fetch(url):
    try:
        return [l for l in requests.get(url, timeout=10).text.splitlines() if l and not l.startswith("#")]
    except: return []

def preprocess_vpn_list(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch, urls))
    raw_list = [item for sublist in results for item in sublist]
    return sorted(set(raw_list))

def get_alive_vpn(vpn_list: list):
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(is_alive, vpn_list))
    alive_list = [line for line, is_ok in zip(vpn_list, results) if is_ok]
    return sorted(set(alive_list))
   

with open("black_list.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(get_alive_vpn(preprocess_vpn_list(black_urls)))))

with open("white_list.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(get_alive_vpn(preprocess_vpn_list(white_urls)))))
