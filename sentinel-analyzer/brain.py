import json
import psycopg2
import requests
import hashlib
import redis
import clickhouse_connect
from kafka import KafkaConsumer
from datetime import datetime

# Motores de Elite
from engines.bot_engine import BotIdentifier
from engines.osint_engine import OSINTAnalyzer
from engines.dpi_engine import DPISignatureDetector
from engines.dlp_engine import DLPEngine
from engines.amp_engine import AMPEngine
from engines.correlation_engine import CorrelationEngine
from engines.soc_orchestrator import SOCOrchestrator

# --- 1. INFRAESTRUTURA ---
try:
    # Redis para Streaming Real-time
    r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

    # PostgreSQL (Persistência de Blacklist)
    conn_pg = psycopg2.connect(
        host="localhost", 
        database="sentinel_vault", 
        user="admin", 
        password="god_eye_password"
    )
    cur_pg = conn_pg.cursor()

    # ClickHouse (Big Data Logs)
    client_ch = clickhouse_connect.get_client(
        host='localhost', port=8123, username='admin', password='god_eye_password'
    )
    
    # Kafka/Redpanda Consumer
    consumer = KafkaConsumer(
        'sentinel-live-traffic',
        bootstrap_servers=['localhost:19092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='sentinel-core-production',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    print("✅ SENTINEL BRAIN: Sistemas Operacionais. Nível Enterprise Ativado.")
except Exception as e:
    print(f"❌ ERRO CRÍTICO INFRA: {e}")
    exit()

# Instanciação dos Motores
bot_engine = BotIdentifier()
osint_engine = OSINTAnalyzer(r)
dpi_engine = DPISignatureDetector()
dlp_engine = DLPEngine()
amp_engine = AMPEngine()
correlation_engine = CorrelationEngine(r)
soc_orchestrator = SOCOrchestrator()

def execute_tier_response(ip, attacker_id, score, reason):
    """Orquestração de Resposta a Incidentes"""
    if score < 40:
        print(f"👀 [MONITOR] {ip} | Score: {score} | Motivo: {reason}")
    elif 40 <= score < 90:
        try:
            requests.post("http://localhost:8080/sync-challenge", json={"ip": ip}, timeout=0.5)
        except: pass
        print(f"⚠️ [CHALLENGE] {ip} sob investigação. Tier 2 Ativado.")
    else:
        # TIER 3: COMANDO DO ARCANJO (Bloqueio Imediato)
        try:
            # 1. Registro Histórico (Postgres)
            cur_pg.execute(
                "INSERT INTO blacklist (ip, reason) VALUES (%s, %s) ON CONFLICT (ip) DO NOTHING", 
                (ip, reason)
            )
            conn_pg.commit()

            # 2. COMANDO DO ARCANJO (Redis - Síncrono e Instantâneo)
            # Isso é o que faz a tela do cara ficar vermelha na hora!
            r.sadd('sentinel:arcanjo:blacklist', ip)
            
            # 3. Broadcast para os Arcanjos de Infra e Backend
            r.publish("arcanjo:broadcast", json.dumps({
                "action": "DROP", 
                "ip": ip, 
                "reason": reason,
                "attacker_id": attacker_id,
                "timestamp": datetime.now().isoformat()
            }))

            # 4. Bloqueio no Ingestor Go
            try:
                requests.post("http://localhost:8080/sync-ban", json={"ip": ip}, timeout=0.5)
            except: 
                pass

            print(f"🚫 [TERMINATED] {ip} neutralizado. Arcanjo assumiu o controle.")
            
            # 5. SOC Counter-Attack (Nmap, Wireshark)
            soc_orchestrator.execute_full_soc_response(ip)
            
        except Exception as e:
            print(f"⚠️ Falha na execução do Arcanjo: {e}")

def generate_attacker_id(event):
    headers = event.get("headers", {})
    fingerprint = f"{event.get('user_agent', '')}|{headers.get('Accept-Language', '')}"
    return hashlib.md5(fingerprint.encode()).hexdigest()

# --- 2. LOOP DE PROCESSAMENTO ---
print("📡 Aguardando tráfego real via Kafka...")

for msg in consumer:
    try:
        event = msg.value
        ip = event["ip"]
        total_score = 0
        reasons = []
        attacker_id = generate_attacker_id(event)

        # 1. Análise de Inteligência (SOC/SIEM)
        misp, msg_m = soc_orchestrator.query_misp(ip)
        if misp: 
            total_score = 100
            reasons.append(msg_m)

        # 2. Motores Técnicos (DPI, BOT, DLP)
        bot_s, bot_m = bot_engine.analyze(event)
        if bot_s > 0:
            total_score += bot_s
            reasons.append(bot_m)

        is_atk, dpi_m, dpi_sev = dpi_engine.scan(event["path"], event.get("body", ""))
        if is_atk:
            total_score = max(total_score, dpi_sev)
            reasons.append(dpi_m)

        # 3. OSINT & GEO (Busca a localização real do IP)
        osint_report = osint_engine.analyze_ip(ip)
        geo_data = osint_report.get("geo", {"lat": 0, "lon": 0, "country": "Local"})

        if osint_report["score"] >= 80:
            total_score = max(total_score, 100)
            reasons.append(f"OSINT: IP Hostil ({geo_data.get('country')})")

        # 4. Correlação de Eventos
        for r_msg in reasons:
            crit, c_msg, h_score = correlation_engine.track_and_correlate(ip, attacker_id, r_msg, total_score)
            if crit:
                total_score = 100
                reasons.append(c_msg)
                break

        # 5. Sentença de Defesa
        if total_score > 0:
            final_reason = " | ".join(list(set(reasons)))
            execute_tier_response(ip, attacker_id, total_score, final_reason)

        # 6. Gravação na Caixa Preta (ClickHouse)
        try:
            client_ch.insert('sentinel_logs.events', [[
                datetime.now(), ip, event["method"], event["path"], 
                event.get("user_agent", ""), json.dumps(event.get("headers", {})), 
                event.get("body", ""), min(total_score, 100), attacker_id
            ]], column_names=['timestamp', 'ip', 'method', 'path', 'user_agent', 'headers', 'body', 'threat_score', 'attacker_id'])
        except Exception as e:
            print(f"⚠️ Erro ClickHouse: {e}")

        # 7. TRANSMISSÃO PRO GLOBO (REDIS)
        map_payload = {
            "ip": ip,
            "threat_score": min(total_score, 100),
            "geo": geo_data,
            "path": event["path"],
            "type": reasons[0] if reasons else "Inbound Request",
            "attacker_id": attacker_id
        }
        r.publish("SENTINEL_GEO_STREAM", json.dumps(map_payload))

        # Log de Console
        status = "🔴" if total_score >= 90 else ("🟡" if total_score >= 40 else "🟢")
        print(f"{status} [{ip}] ID: {attacker_id[:8]} | Score: {total_score}% | Geo: {geo_data.get('country')}")

    except Exception as e:
        print(f"❌ FALHA NO CICLO: {e}")