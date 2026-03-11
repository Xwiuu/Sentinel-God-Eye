import json
import psycopg2
import requests
import hashlib
import redis
import clickhouse_connect
from kafka import KafkaConsumer
from datetime import datetime

# Importando seus Motores de Elite
from engines.bot_engine import BotIdentifier
from engines.osint_engine import OSINTAnalyzer
from engines.dpi_engine import DPISignatureDetector
from engines.dlp_engine import DLPEngine
from engines.amp_engine import AMPEngine

# --- 1. CONEXÕES DE INFRAESTRUTURA ---
try:
    r = redis.Redis(host="localhost", port=6379, db=0) # Mantemos para Cache e Stream pro Vue.js
    
    # O Cemitério Oficial (PostgreSQL)
    conn_pg = psycopg2.connect(host="localhost", database="sentinel_vault", user="admin", password="god_eye_password")
    cur_pg = conn_pg.cursor()

    # A Caixa Preta de Logs (ClickHouse)
    client_ch = clickhouse_connect.get_client(host='localhost', port=8123, username='admin', password='god_eye_password')
    
    # O Tubo de Dados (Kafka)
    consumer = KafkaConsumer(
        'sentinel-live-traffic',
        bootstrap_servers=['localhost:19092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='sentinel-brain-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    print("✅ SENTINEL BRAIN: Conectado ao Kafka, Postgres e ClickHouse. Operando em Nível Enterprise.")
except Exception as e:
    print(f"❌ ERRO INFRA: {e}")
    exit()

# Instancia os Motores
bot_engine = BotIdentifier()
osint_engine = OSINTAnalyzer(r)
dpi_engine = DPISignatureDetector()
dlp_engine = DLPEngine()
amp_engine = AMPEngine()

def execute_ban(ip, reason):
    """Aplica a sentença final no Postgres e corta a conexão no Go"""
    try:
        cur_pg.execute("INSERT INTO blacklist (ip, reason) VALUES (%s, %s) ON CONFLICT (ip) DO NOTHING", (ip, reason))
        conn_pg.commit()
        requests.post("http://localhost:8080/sync-ban", json={"ip": ip}, timeout=0.5)
        print(f"🚫 [BAN TERMINATED] {ip} | Motivo: {reason}")
    except Exception as e:
        print(f"⚠️ Erro ao banir: {e}")

def generate_attacker_id(event):
    """Gera a Digital Única do Atacante (Mesmo se ele mudar de IP)"""
    # Usamos o User-Agent + Accept-Language como base do fingerprint
    headers = event.get("headers", {})
    fingerprint_raw = f"{event.get('user_agent', '')}|{headers.get('Accept-Language', '')}|{headers.get('Accept-Encoding', '')}"
    return hashlib.md5(fingerprint_raw.encode()).hexdigest()

# --- 2. LOOP PRINCIPAL (KAFKA CONSUMER) ---
print("📡 Escutando tráfego de alta velocidade...")

for msg in consumer:
    event = msg.value
    ip = event["ip"]
    total_score = 0
    reasons = []

    # O FINGERPRINT (Attacker ID)
    attacker_id = generate_attacker_id(event)

    # 1. BOT ID
    bot_score, bot_msg = bot_engine.analyze(event)
    if bot_score > 0:
        total_score += bot_score
        reasons.append(bot_msg)

    # 2. DPI (Assinaturas e Injeções)
    is_attack, dpi_msg, dpi_severity = dpi_engine.scan(event["path"], event.get("body", ""))
    if is_attack:
        total_score = max(total_score, dpi_severity)
        reasons.append(dpi_msg)

    # 3. DLP (Vazamento de Dados na Saída/Entrada)
    is_leak, dlp_msg, dlp_severity = dlp_engine.inspect(event.get("body", ""))
    if is_leak:
        total_score = max(total_score, dlp_severity)
        reasons.append(dlp_msg)

    # 4. AMP (Análise de Malware em POST)
    if event["method"] == "POST":
        is_malware, amp_msg, amp_severity = amp_engine.analyze_file(event.get("body", ""))
        if is_malware:
            total_score = max(total_score, amp_severity)
            reasons.append(amp_msg)

    # 5. OSINT (Reputação Global - Chamado por último para economizar API)
    osint_report = osint_engine.analyze_ip(ip)
    if osint_report["score"] >= 80:
        total_score = max(total_score, 100)
        reasons.append(f"OSINT: IP Hostil Confirmado ({osint_report['geo']['country']})")

    # --- EXECUÇÃO DA SENTENÇA ---
    if total_score >= 90:
        final_reason = " | ".join(reasons)
        execute_ban(ip, final_reason)

    # --- REGISTRO NA CAIXA PRETA (CLICKHOUSE) ---
    try:
        log_time = datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        client_ch.insert('sentinel_logs.events', [[
            log_time, 
            ip, 
            event["method"], 
            event["path"], 
            event.get("user_agent", ""), 
            json.dumps(event.get("headers", {})), 
            event.get("body", ""), 
            min(total_score, 100), 
            attacker_id
        ]], column_names=['timestamp', 'ip', 'method', 'path', 'user_agent', 'headers', 'body', 'threat_score', 'attacker_id'])
    except Exception as e:
        print(f"⚠️ Erro ao salvar no ClickHouse: {e}")

    # --- STREAM PRO FRONT-END ---
    event["threat_score"] = min(total_score, 100)
    event["geo"] = osint_report["geo"]
    event["attacker_id"] = attacker_id
    r.publish("SENTINEL_GEO_STREAM", json.dumps(event))

    # Log no terminal
    status = "🔴" if total_score >= 90 else "🟢"
    print(f"{status} [{ip}] ID: {attacker_id[:8]} | Score: {total_score}% | Via: Kafka -> ClickHouse")