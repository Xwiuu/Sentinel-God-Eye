import re

class DLPEngine:
    def __init__(self):
        # Assinaturas de dados que NUNCA devem estar em tráfego aberto
        self.sensitive_patterns = {
            "BRAZILIAN_CPF": r"\d{3}\.\d{3}\.\d{3}-\d{2}",
            "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
            "PRIVATE_KEY": r"-----BEGIN (RSA|OPENSSH|PRIVATE) KEY-----",
            "SENSITIVE_EMAIL": r"[\w\.-]+@(governo\.br|empresa\.com\.br|admin\.com)",
            "SQL_DUMP": r"(INSERT INTO|CREATE TABLE|DROP DATABASE)" # Previne exportação de DB
        }

    def inspect(self, content):
        """Varre o conteúdo em busca de dados protegidos"""
        findings = []
        severity = 0

        for label, pattern in self.sensitive_patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                findings.append(f"{label} ({len(matches)}x)")
                severity = 100 # Vazamento de dado sensível é prioridade máxima
        
        if findings:
            return True, f"DLP ALERT: Vazamento de dados detectado: {', '.join(findings)}", severity
        
        return False, "No data leak detected", 0