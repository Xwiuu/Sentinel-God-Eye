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

    def _check_shodan(self, ip):
        """Extrai dados detalhados do Shodan: Portas, Serviços, Vulnerabilidades"""
        try:
            r = requests.get(f"https://api.shodan.io/shodan/host/{ip}?key={self.keys['shodan']}", timeout=5).json()
            
            # Extraindo os nomes dos equipamentos e banners
            services = []
            for item in r.get('data', []):
                port = item.get('port')
                product = item.get('product', 'Unknown Service')
                services.append(f"Port {port}: {product}")

            return {
                "ports": r.get('ports', []),
                "hostnames": r.get('hostnames', []),
                "os": r.get('os', 'Undetected'),
                "org": r.get('org', 'Unknown'),
                "isp": r.get('isp', 'Unknown'),
                "services": services[:5], # Pega os 5 primeiros serviços
                "vulns": r.get('vulns', [])
            }
        except Exception as e:
            print(f"⚠️ [SHODAN] Erro ao consultar: {e}")
            return {"ports": [], "hostnames": [], "services": [], "vulns": []}

    def analyze_ip(self, ip):
        """Varredura Completa: Reputação, Infraestrutura e Geolocalização"""
        
        # 1. Tenta buscar no Cache (Velocidade de Flash)
        cached = self._get_cache(ip)
        if cached:
            print(f"💾 [CACHE HIT] Dados do {ip} carregados do Redis")
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
                if report["is_proxy"]: 
                    report["score"] += 40
                    print(f"🚨 [PROXY DETECTED] {ip} é VPN/Proxy/Tor")
        except Exception as e:
            print(f"⚠️ [PROXYCHECK] {e}")

        # --- MÓDULO B: FICHA CRIMINAL (ABUSEIPDB) ---
        if self.keys["abuse_ipdb"] != "COLE_SUA_CHAVE_AQUI":
            try:
                headers = {'Accept': 'application/json', 'Key': self.keys["abuse_ipdb"]}
                params = {'ipAddress': ip, 'maxAgeInDays': '90'}
                res = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params, timeout=3).json()
                abuse_score = res['data']['abuseConfidenceScore']
                report["osint_data"]["abuse_score"] = abuse_score
                if abuse_score > 50: 
                    report["score"] += 60 # Confirmação de Ameaça
                    print(f"⚠️ [ABUSEIPDB] {ip} tem score de abuso: {abuse_score}%")
            except Exception as e:
                print(f"⚠️ [ABUSEIPDB] {e}")

        # --- MÓDULO C: EXPOSIÇÃO DE PORTAS (SHODAN) ---
        if self.keys["shodan"] != "COLE_SUA_CHAVE_AQUI":
            shodan_data = self._check_shodan(ip)
            report["osint_data"]["shodan"] = shodan_data
            if len(shodan_data.get("ports", [])) > 5: 
                report["score"] += 20 # Muitos serviços abertos = Scanner
                print(f"🔓 [SHODAN] {ip} possui {len(shodan_data['ports'])} portas abertas")

        # Normaliza o Score Máximo em 100
        report["score"] = min(report["score"], 100)
        report["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 3. Salva na Memória de Curto Prazo
        self._set_cache(ip, report)
        
        print(f"✅ [FORENSICS] Análise completa de {ip} - Score: {report['score']}")
        return report