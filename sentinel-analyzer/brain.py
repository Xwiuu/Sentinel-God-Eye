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
from engines.correlation_engine import CorrelationEngine

# NOVA INTEGRAÇÃO SOC (100% Completo Nível Militar)
from engines.soc_orchestrator import SOCOrchestrator

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
correlation_engine = CorrelationEngine(r)

# Instancia o Orquestrador SOC Supremo
soc_orchestrator = SOCOrchestrator()

def execute_tier_response(ip, attacker_id, score, reason):
    """SISTEMA DE MITIGAÇÃO PROGRESSIVA COM INTEGRAÇÕES SOC"""
    if score < 40:
        # TIER 1 - Apenas Observação (Log Mode)
        print(f"👀 [LOG] {ip} suspeito, mas abaixo do limiar. Motivo: {reason}")
        
    elif 40 <= score < 90:
        # TIER 2 - Desafio (Challenge)
        try:
            requests.post("http://localhost:8080/sync-challenge", json={"ip": ip}, timeout=0.5)
        except:
            pass
        print(f"⚠️ [CHALLENGE] {ip} atingiu TIER 2. Enviando desafio JavaScript. Motivo: {reason}")
        
    else:
        # TIER 3 - BANIMENTO E CONTRA-MEDIDAS
        try:
            # 1. Aplica o Ban
            cur_pg.execute("INSERT INTO blacklist (ip, reason) VALUES (%s, %s) ON CONFLICT (ip) DO NOTHING", (ip, reason))
            conn_pg.commit()
            requests.post("http://localhost:8080/sync-ban", json={"ip": ip}, timeout=0.5)
            print(f"🚫 [BAN TERMINATED] {ip} (ID: {attacker_id[:8]}) neutralizado! Motivo: {reason}")
            
            # 2. APERTA O BOTÃO VERMELHO! (Chama Nmap, Wireshark, OpenVAS e Metasploit de uma vez)
            soc_orchestrator.execute_full_soc_response(ip)
            
        except Exception as e:
            print(f"⚠️ Erro no Tier 3: {e}")

def generate_attacker_id(event):
    """Gera a Digital Única do Atacante (Mesmo se ele mudar de IP)"""
    # Usamos o User-Agent + Accept-Language como base do fingerprint
    headers = event.get("headers", {})
    fingerprint_raw = f"{event.get('user_agent', '')}|{headers.get('Accept-Language', '')}|{headers.get('Accept-Encoding', '')}"
    return hashlib.md5(fingerprint_raw.encode()).hexdigest()

# --- 2. LOOP PRINCIPAL (KAFKA CONSUMER) ---
print("📡 Escutando tráfego de alta velocidade com Integrações SOC Ativas...")

for msg in consumer:
    event = msg.value
    ip = event["ip"]
    total_score = 0
    reasons = []

    # O FINGERPRINT (Attacker ID)
    attacker_id = generate_attacker_id(event)

    # 0. INTELIGÊNCIA GLOBAL E SIEM (MISP, Wazuh, Security Onion/Suricata/Zeek)
    is_misp, misp_msg = soc_orchestrator.query_misp(ip)
    is_wazuh, wazuh_msg = soc_orchestrator.query_wazuh(ip)
    is_onion, onion_msg = soc_orchestrator.query_security_onion(ip)
    
    if is_misp: 
        total_score = 100
        reasons.append(misp_msg)
    if is_wazuh: 
        total_score = 100
        reasons.append("WAZUH ALERT: Invasão de Host Detectada")
    if is_onion: 
        total_score = max(total_score, 80)
        reasons.append(onion_msg)

    # 1. BOT ID
    bot_score, bot_msg = bot_engine.analyze(event)
    if bot_score > 0:
        total_score += bot_score
        if bot_msg not in reasons: reasons.append(bot_msg)

    # 2. DPI (Assinaturas e Injeções)
    is_attack, dpi_msg, dpi_severity = dpi_engine.scan(event["path"], event.get("body", ""))
    if is_attack:
        total_score = max(total_score, dpi_severity)
        if dpi_msg not in reasons: reasons.append(dpi_msg)

    # 3. DLP (Vazamento de Dados na Saída/Entrada)
    is_leak, dlp_msg, dlp_severity = dlp_engine.inspect(event.get("body", ""))
    if is_leak:
        total_score = max(total_score, dlp_severity)
        if dlp_msg not in reasons: reasons.append(dlp_msg)

    # 4. AMP (Análise de Malware em POST)
    if event["method"] == "POST":
        is_malware, amp_msg, amp_severity = amp_engine.analyze_file(event.get("body", ""))
        if is_malware:
            total_score = max(total_score, amp_severity)
            if amp_msg not in reasons: reasons.append(amp_msg)

    # 5. OSINT (Reputação Global - Chamado por último para economizar API)
    osint_report = osint_engine.analyze_ip(ip)
    if osint_report["score"] >= 80:
        total_score = max(total_score, 100)
        osint_msg = f"OSINT: IP Hostil Confirmado ({osint_report['geo']['country']})"
        if osint_msg not in reasons: reasons.append(osint_msg)

    # --- 6. MOTOR DE CORRELAÇÃO ---
    for alert_reason in reasons:
        is_critical, corr_msg, historical_score = correlation_engine.track_and_correlate(ip, attacker_id, alert_reason, total_score)
        if is_critical:
            total_score = 100
            if corr_msg not in reasons: reasons.append(corr_msg)
            break 

    # --- EXECUÇÃO DA SENTENÇA (SISTEMA DE TIERS) ---
    if total_score > 0:
        final_reason = " | ".join(reasons)
        execute_tier_response(ip, attacker_id, total_score, final_reason)

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
    status = "🔴" if total_score >= 90 else ("🟡" if total_score >= 40 else "🟢")
    print(f"{status} [{ip}] ID: {attacker_id[:8]} | Score: {total_score}% | Via: Kafka -> ClickHouse")