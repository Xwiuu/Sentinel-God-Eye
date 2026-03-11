import re

class BotIdentifier:
    def __init__(self):
        # Assinaturas de Bots conhecidos e Scanners
        self.bad_uas = ["PYTHON", "GO-HTTP", "NMAP", "CURL", "SQLMAP", "NIKTO", "PUPPETEER", "HEADLESSCHROME"]

    def analyze(self, event): # <--- Olha o nome certinho aqui!
        score = 0
        ua = event.get('user_agent', '').upper()
        headers = event.get('headers', {})
        
        # 1. Assinatura Direta de Ferramenta
        for bad_ua in self.bad_uas:
            if bad_ua in ua: 
                return 100, f"Bot Tool Detectado: {bad_ua}"

        # 2. Comportamento de Bot: Falta de Header Humano
        # Navegadores reais SEMPRE enviam Accept-Language
        if "Accept-Language" not in headers and "ACCEPT-LANGUAGE" not in headers:
            score += 40
        
        # 3. Bots costumam ignorar o header de Referência em POSTs
        if event.get('method') == "POST" and "Referer" not in headers and "REFERER" not in headers:
            score += 50

        if score > 0:
            return score, "Comportamento de Automação Detectado"
            
        return 0, "Humano"