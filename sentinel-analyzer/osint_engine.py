import requests
import json

# Suas chaves de acesso (Deixe vazio se ainda não criou, o sistema não vai travar)
ABUSE_IPDB_KEY = "COLE_SUA_CHAVE_ABUSE_AQUI"
SHODAN_KEY = "COLE_SUA_CHAVE_SHODAN_AQUI"

def is_local(ip):
    """Ignora varreduras em IPs locais e de testes"""
    return ip == "127.0.0.1" or ip.startswith("192.168.") or ip.startswith("10.")

def check_abuseipdb(ip, redis_client):
    """Consulta a ficha criminal global do atacante"""
    if is_local(ip) or not ABUSE_IPDB_KEY: return 0
    
    cached_score = redis_client.get(f"osint:abuse:{ip}")
    if cached_score: return int(cached_score)

    try:
        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {'Accept': 'application/json', 'Key': ABUSE_IPDB_KEY}
        resp = requests.get(url, headers=headers, params={'ipAddress': ip, 'maxAgeInDays': '90'}, timeout=3)
        if resp.status_code == 200:
            score = resp.json()['data']['abuseConfidenceScore']
            redis_client.setex(f"osint:abuse:{ip}", 86400, score)
            return score
    except: pass
    return 0

def check_shodan(ip, redis_client):
    """Faz um Raio-X do IP para descobrir portas e vulnerabilidades"""
    if is_local(ip) or not SHODAN_KEY: return None
    
    cached_data = redis_client.get(f"osint:shodan:{ip}")
    if cached_data: return json.loads(cached_data)

    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_KEY}"
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            info = {"ports": data.get('ports', []), "org": data.get('org', 'Unknown')}
            redis_client.setex(f"osint:shodan:{ip}", 86400, json.dumps(info))
            return info
    except: pass
    return None

def check_vpn_tor(ip, redis_client):
    """Fura-Máscaras: Verifica se é VPN, Proxy ou Tor"""
    if is_local(ip): return False, "Rede Local"
    
    cached_data = redis_client.get(f"osint:vpn:{ip}")
    if cached_data: 
        return cached_data.decode('utf-8') == 'True', "Cached Mask"

    try:
        url = f"http://proxycheck.io/v2/{ip}?vpn=1&asn=1"
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if ip in data and data[ip].get('proxy') == 'yes':
                proxy_type = data[ip].get('type', 'VPN/Proxy')
                redis_client.setex(f"osint:vpn:{ip}", 86400, "True")
                return True, proxy_type
            else:
                redis_client.setex(f"osint:vpn:{ip}", 86400, "False")
                return False, "IP Residencial"
    except: pass
    return False, "Desconhecido"

def get_geolocation(ip, redis_client):
    """Radar de Precisão Máxima (Máximo permitido sem mandado judicial)"""
    if is_local(ip): 
        return {"lat": -23.5505, "lon": -46.6333, "country": "BR", "city": "Bunker", "isp": "Localhost"}
    
    cached_geo = redis_client.get(f"osint:geo:{ip}")
    if cached_geo: return json.loads(cached_geo)

    try:
        # Pede os dados completos: Cidade, CEP (ZIP), ISP e Coordenadas
        url = f"http://ip-api.com/json/{ip}?fields=status,country,city,zip,lat,lon,isp"
        resp = requests.get(url, timeout=3)
        
        if resp.status_code == 200:
            data = resp.json()
            if data['status'] == 'success':
                geo_info = {
                    "lat": data.get('lat', 0.0),
                    "lon": data.get('lon', 0.0),
                    "country": data.get('country', 'Unknown'),
                    "city": data.get('city', 'Unknown'),
                    "zip": data.get('zip', 'N/A'),
                    "isp": data.get('isp', 'Unknown')
                }
                redis_client.setex(f"osint:geo:{ip}", 86400, json.dumps(geo_info))
                return geo_info
    except: pass
    return {"lat": 0.0, "lon": 0.0, "country": "Unknown", "city": "Unknown", "isp": "Unknown"}