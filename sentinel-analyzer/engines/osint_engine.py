import requests
import json
import time

class OSINTAnalyzer:
    def __init__(self, redis_client):
        self.r = redis_client
        # API KEYS (Coloque as suas aqui ou deixe vazio para usar apenas os módulos free)
        self.keys = {
            "abuse_ipdb": "COLE_SUA_CHAVE_AQUI",
            "shodan": "COLE_SUA_CHAVE_AQUI",
            "proxycheck": "COLE_SUA_CHAVE_AQUI" # Free até 1000 requests/dia
        }

    def _get_cache(self, key):
        data = self.r.get(f"osint:cache:{key}")
        return json.loads(data) if data else None

    def _set_cache(self, key, data, ttl=86400): # Cache de 24 horas padrão
        self.r.setex(f"osint:cache:{key}", ttl, json.dumps(data))

    def analyze_ip(self, ip):
        """Varredura Completa: Reputação, Infraestrutura e Geolocalização"""
        
        # 1. Tenta buscar no Cache (Velocidade de Flash)
        cached = self._get_cache(ip)
        if cached:
            return cached

        # 2. Inicia Inteligência de Campo
        report = {
            "score": 0,
            "is_proxy": False,
            "type": "Residential",
            "geo": {"country": "Unknown", "city": "Unknown", "isp": "Unknown"},
            "osint_data": {}
        }

        # --- MÓDULO A: GEOLOCALIZAÇÃO E PROXY (FREE) ---
        try:
            # Usando ProxyCheck para pegar se é VPN/Tor e Geo ao mesmo tempo
            url = f"https://proxycheck.io/v2/{ip}?key={self.keys['proxycheck']}&vpn=1&asn=1&node=1"
            resp = requests.get(url, timeout=3).json()
            
            if ip in resp:
                data = resp[ip]
                report["is_proxy"] = data.get("proxy") == "yes"
                report["type"] = data.get("type", "Residential")
                report["geo"] = {
                    "country": data.get("isocode", "??"),
                    "city": data.get("city", "Unknown"),
                    "isp": data.get("asn", "Unknown")
                }
                if report["is_proxy"]: report["score"] += 40
        except: pass

        # --- MÓDULO B: FICHA CRIMINAL (ABUSEIPDB) ---
        if self.keys["abuse_ipdb"] != "COLE_SUA_CHAVE_AQUI":
            try:
                headers = {'Accept': 'application/json', 'Key': self.keys["abuse_ipdb"]}
                params = {'ipAddress': ip, 'maxAgeInDays': '90'}
                res = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params, timeout=3).json()
                abuse_score = res['data']['abuseConfidenceScore']
                report["osint_data"]["abuse_score"] = abuse_score
                if abuse_score > 50: report["score"] += 60 # Confirmação de Ameaça
            except: pass

        # --- MÓDULO C: EXPOSIÇÃO DE PORTAS (SHODAN) ---
        if self.keys["shodan"] != "COLE_SUA_CHAVE_AQUI":
            try:
                res = requests.get(f"https://api.shodan.io/shodan/host/{ip}?key={self.keys['shodan']}", timeout=3).json()
                report["osint_data"]["ports"] = res.get("ports", [])
                report["osint_data"]["org"] = res.get("org", "Unknown")
                if len(report["osint_data"]["ports"]) > 5: report["score"] += 20 # Muitos serviços abertos = Scanner
            except: pass

        # Normaliza o Score Máximo em 100
        report["score"] = min(report["score"], 100)
        
        # 3. Salva na Memória de Curto Prazo
        self._set_cache(ip, report)
        
        return report