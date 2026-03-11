import hashlib
import re

class AMPEngine:
    def __init__(self):
        # Banco de dados local de Hashes conhecidos como Malwares (Exemplos)
        # Em um cenário real, aqui você consultaria uma API como VirusTotal
        self.malware_hashes = {
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Empty File Attack",
            "5f4dcc3b5aa765d61d8327deb882cf99": "Old PHP Shell Signature"
        }
        
        # Heurística: Padrões comuns em Webshells (PHP, ASPX, JSP)
        self.webshell_patterns = [
            r"eval\(\$_POST\[.*\]\)", 
            r"system\(\$_GET\[.*\]\)",
            r"shell_exec\(.*\)",
            r"base64_decode\(['\"]([A-Za-z0-9+/]{40,})['\"]", # Scripts ofuscados
            r"passthru\(",
            r"python_set_user"
        ]

    def analyze_file(self, file_content):
        """Analisa o conteúdo binário ou textual de um upload"""
        if not file_content or len(file_content) < 10:
            return False, "Clean", 0

        # 1. GERAÇÃO DE DNA (SHA-256)
        file_hash = hashlib.sha256(file_content.encode() if isinstance(file_content, str) else file_content).hexdigest()
        
        # 2. CHECK NA BLACKLIST DE HASHES
        if file_hash in self.malware_hashes:
            return True, f"AMP ALERT: Malware Conhecido Detectado ({self.malware_hashes[file_hash]})", 100

        # 3. ANÁLISE HEURÍSTICA (Procura por 'Células Cancerosas' no código)
        content_str = str(file_content).upper()
        for pattern in self.webshell_patterns:
            if re.search(pattern, content_str, re.IGNORECASE):
                return True, "AMP ALERT: Webshell/Backdoor detectado via Heurística", 100

        return False, "File looks safe", 0