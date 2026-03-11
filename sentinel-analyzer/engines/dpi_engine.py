import re
import urllib.parse

class DPISignatureDetector:
    def __init__(self):
        # Base de Conhecimento: Assinaturas de Ataque (Regex de Elite)
        self.signatures = {
            "SQL_INJECTION": [
                r"(UNION\s+SELECT|SELECT\s+.*\s+FROM)", 
                r"(\bDROP\s+TABLE\b|\bDELETE\s+FROM\b|\bUPDATE\s+.*\s+SET\b)",
                r"(OR\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?)", # Bypass de login clássico
                r"(--|#|\/\*|;)\s*$", # Comentários de SQL
                r"(SLEEP\(.*\)|BENCHMARK\(.*\))" # Blind SQL Injection (Time-based)
            ],
            "XSS_ATTACK": [
                r"(<script.*?>.*?<\/script>)",
                r"(onerror\s*=|onload\s*=|onclick\s*=)",
                r"(javascript:.*\(.*\))",
                r"(<iframe.*?>| <embed.*?>)"
            ],
            "PATH_TRAVERSAL": [
                r"(\.\.\/|\.\.\\)", # Tentativa de subir pastas
                r"(/etc/passwd|/etc/shadow|/etc/group)", # Alvos Linux
                r"(C:\\Windows\\System32\\config)", # Alvos Windows
                r"(proc/self/environ)"
            ],
            "REMOTE_CODE_EXECUTION": [
                r"(\bNC\s+-E\b|\bBASH\s+-I\b|\bPHPINFO\(\)\b)",
                r"(\bSYSTEM\(.*\)\b|\bEXEC\(.*\)\b|\bPASSTHRU\(.*\)\b)",
                r"(WGET\s+http|CURL\s+http)" # Download de malware
            ]
        }

    def scan(self, path, body):
        """Varredura Profunda: Analisa URL e Corpo da Requisição"""
        # Decodifica a URL (Ex: transforma %20 em espaço)
        decoded_path = urllib.parse.unquote(path).upper()
        decoded_body = urllib.parse.unquote(body).upper()
        
        full_content = f"{decoded_path} {decoded_body}"
        
        hits = []
        severity = 0

        for attack_type, patterns in self.signatures.items():
            for pattern in patterns:
                if re.search(pattern, full_content, re.IGNORECASE):
                    hits.append(attack_type)
                    severity = 100 # Se bateu em Regex de DPI, é 100% Hostil
                    break # Encontrou um padrão, pula para o próximo tipo de ataque
        
        if hits:
            return True, f"DPI Alert: {', '.join(hits)} Detected", severity
        
        return False, "Clean Payload", 0