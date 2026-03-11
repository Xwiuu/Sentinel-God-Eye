import redis
import json
import time

# Conecta ao Fluxo de Sangue
r = redis.Redis(host='localhost', port=6379, db=0)

# O Arsenal (IPs reais conhecidos por ataques e um inocente no meio)
attackers = [
    {"ip": "185.220.101.46", "path": "/admin/login", "desc": "Nó de Saída do Tor (Alemanha)"},
    {"ip": "45.134.144.120", "path": "/?search=UNION SELECT", "desc": "Servidor Suspeito (Rússia)"},
    {"ip": "103.145.13.133", "path": "/etc/passwd", "desc": "Scanner de Vulnerabilidade (China)"},
    {"ip": "8.8.8.8", "path": "/index.html", "desc": "Visitante Inocente de Cara Limpa (EUA)"},
    {"ip": "192.42.116.16", "path": "/api/users?id=1 OR 1=1", "desc": "VPN Mascarada (Holanda)"}
]

print("🔥 [GOD EYE] INICIANDO SIMULAÇÃO DE ATAQUE GLOBAL...")
print("Despejando tráfego inimigo na rede...\n")

for attacker in attackers:
    print(f"🚀 Disparando pacote de: {attacker['desc']} | IP: {attacker['ip']}")
    
    # Monta a carga (payload) fingindo ser o Go enviando
    event = {
        "project": "bunker_core",
        "ip": attacker["ip"],
        "path": attacker["path"],
        "user_agent": "Mozilla/5.0 (Hacker-Bot/1.0)",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "threat_score": 0
    }
    
    # Injeta no Redis para o Python (brain.py) analisar
    r.publish('SENTINEL_LIVE_STREAM', json.dumps(event))
    
    # Pausa de 3 segundos para você ver o terminal do Python "pensar" e bater nas APIs
    time.sleep(3) 

print("\n🏁 Rajada concluída! Vá conferir os corpos no terminal do Cérebro e no DBeaver.")