import requests
import json
import redis

class OSINTAnalyzer:
    def __init__(self, redis_client):
        self.r = redis_client
        # SUAS CHAVES REAIS
        self.ABUSE_IPDB_KEY = "233048731d10813248bbda917ce4cc5b3cf24787a0e715e1804198be10976922fee892f7b8daac21"
        self.SHODAN_KEY = "bN39vv2zjplx12Ec3mVZk4einpSgE0bd"

    def analyze_ip(self, ip):
        """Executa a perícia completa no alvo"""
        if ip == "127.0.0.1" or ip.startswith("192.168."):
            return {
                "score": 0,
                "geo": {"country": "Localhost", "city": "Bunker", "isp": "Internal Network", "lat": -23.5, "lon": -46.6},
                "abuse": {"score": 0, "reports": 0},
                "shodan": {"ports": [], "os": "Unknown", "vulns": []}
            }

        # 1. GEOLOCALIZAÇÃO
        geo = self._get_geo(ip)
        
        # 2. ABUSO CRIMINAL (AbuseIPDB)
        abuse = self._check_abuse(ip)
        
        # 3. RAIO-X DE INFRAESTRUTURA (Shodan)
        shodan = self._check_shodan(ip)

        return {
            "ip": ip,
            "score": abuse['score'],
            "geo": geo,
            "abuse": abuse,
            "shodan": shodan
        }

    def _get_geo(self, ip):
        cache = self.r.get(f"osint:geo:{ip}")
        if cache: return json.loads(cache)
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon,isp,proxy", timeout=3).json()
            if r['status'] == 'success':
                self.r.setex(f"osint:geo:{ip}", 86400, json.dumps(r))
                return r
        except: pass
        return {"country": "Unknown"}

    def _check_abuse(self, ip):
        try:
            url = "https://api.abuseipdb.com/api/v2/check"
            headers = {'Accept': 'application/json', 'Key': self.ABUSE_IPDB_KEY}
            params = {'ipAddress': ip, 'maxAgeInDays': '90'}
            r = requests.get(url, headers=headers, params=params, timeout=4).json()
            return {
                "score": r['data']['abuseConfidenceScore'],
                "total_reports": r['data']['totalReports'],
                "last_report": r['data'].get('lastReportedAt', 'N/A')
            }
        except: return {"score": 0, "total_reports": 0}

    def _check_shodan(self, ip):
        try:
            r = requests.get(f"https://api.shodan.io/shodan/host/{ip}?key={self.SHODAN_KEY}", timeout=5).json()
            return {
                "ports": r.get('ports', []),
                "os": r.get('os', 'Unknown'),
                "vulns": r.get('vulns', []), # LISTA DE CVEs (Vulnerabilidades reais)
                "org": r.get('org', 'Unknown')
            }
        except: return {"ports": [], "vulns": []}