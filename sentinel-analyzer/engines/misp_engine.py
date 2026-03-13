import requests
import json

class MISPEngine:
    def __init__(self, redis_client):
        self.r = redis_client
        # URL do seu servidor MISP ou de um Feed Open Source de IoCs (Indicators of Compromise)
        self.misp_url = "https://misp.suaempresa.com/attributes/restSearch"
        self.api_key = "SUA_CHAVE_MISP_AQUI"
        self.headers = {
            "Authorization": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def check_ip(self, ip):
        """Verifica se o IP está na lista de criminosos globais do MISP"""
        # 1. Verifica no Cache do Redis primeiro (para ser ultra-rápido)
        if self.r.sismember("misp_blacklist_cache", ip):
            return True, "MISP ALERT: IP listado em feeds de Threat Intelligence Globais"

        # 2. Se quiser consultar em tempo real (opcional, melhor rodar um job de atualização de madrugada)
        try:
            payload = {"value": ip, "type": "ip-src"}
            response = requests.post(self.misp_url, headers=self.headers, json=payload, timeout=2)
            if response.status_code == 200 and len(response.json().get("response", {}).get("Attribute", [])) > 0:
                self.r.sadd("misp_blacklist_cache", ip) # Salva no cache
                return True, "MISP ALERT: IP detectado na base do MISP agora!"
        except:
            pass
            
        return False, ""