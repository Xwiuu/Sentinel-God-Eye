import json
import asyncio
import psycopg2
import redis
import requests
import psutil
import clickhouse_connect
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from ipwhois import IPWhois
from engines.osint_engine import OSINTAnalyzer

# --- CONFIGURAÇÃO CORE ---
app = FastAPI(title="Sentinel God Eye - Satellite Node")


# Liberando Geral (CORS) para o seu Dashboard Vue não ser bloqueado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- GERENCIADOR DE CONEXÕES REAL-TIME ---
class ConnectionManager:
    def __init__(self):
        # Lista de operadores (navegadores) conectados
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(
            f"📡 [SATÉLITE] Novo Operador Conectado. Total: {len(self.active_connections)}"
        )

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(
                f"📡 [SATÉLITE] Operador Desconectado. Restantes: {len(self.active_connections)}"
            )

    async def broadcast(self, message: str):
        """Dispara os dados para todos os Dashboards abertos"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Se a conexão caiu, o loop ignora e segue
                pass


manager = ConnectionManager()


# --- INTEGRAÇÃO COM CLICKHOUSE (HISTÓRICO) ---
def get_ch_client():
    return clickhouse_connect.get_client(
        host="localhost", port=8123, username="admin", password="god_eye_password"
    )


@app.get("/api/history")
async def get_history():
    """Puxa a 'Caixa Preta' para o Dashboard carregar já cheio de dados"""
    try:
        client = get_ch_client()
        query = "SELECT * FROM sentinel_logs.events ORDER BY timestamp DESC LIMIT 60"
        result = client.query(query)

        history = []
        for row in result.result_rows:
            item = dict(zip(result.column_names, row))
            # Tratamento de data para JSON
            if hasattr(item["timestamp"], "isoformat"):
                item["timestamp"] = item["timestamp"].isoformat()

            # Decodifica headers se vierem como string
            if isinstance(item.get("headers"), str):
                try:
                    item["headers"] = json.loads(item["headers"])
                except:
                    item["headers"] = {}
            history.append(item)

        print(f"📦 [SÉTIMA FROTA] Histórico extraído: {len(history)} eventos enviados.")
        return history
    except Exception as e:
        print(f"❌ [ERRO CRÍTICO CH] Falha ao ler ClickHouse: {e}")
        return []


# --- LISTENER DO REDIS (PONTE BRAIN -> SATELLITE) ---
async def redis_listener():
    """Escuta o canal SENTINEL_GEO_STREAM e repassa para o WebSocket"""
    r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("SENTINEL_GEO_STREAM")

    print("🚀 [SATÉLITE] Escutando fluxo do Brain... Transmissão iniciada.")

    async for message in pubsub.listen():
        if message["type"] == "message":
            # Broadcast imediato para o Front-end
            await manager.broadcast(message["data"])


# --- EVENTOS DE STARTUP ---
@app.on_event("startup")
async def startup_event():
    # Inicia o listener do Redis em background
    asyncio.create_task(redis_listener())


# --- ENDPOINT WEBSOCKET ---
@app.websocket("/ws/threat-stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Mantém a conexão viva escutando pings vazios
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"⚠️ [SATELLITE] Erro na conexão WS: {e}")
        manager.disconnect(websocket)


@app.get("/api/explorer")
async def get_explorer_data(ip: str = None, threat_type: str = None):
    print(f"🔍 [EXPLORER] Query recebida - IP: {ip}, Type: {threat_type}")
    try:
        # Criamos a conexão aqui dentro para garantir que está viva
        client_ch = clickhouse_connect.get_client(
            host="localhost", port=8123, username="admin", password="god_eye_password"
        )

        query = "SELECT * FROM sentinel_logs.events WHERE 1=1"
        if ip:
            query += f" AND ip LIKE '%{ip}%'"
        if threat_type:
            # Se você estiver filtrando por path ou motivo
            query += (
                f" AND (path LIKE '%{threat_type}%' OR body LIKE '%{threat_type}%')"
            )

        query += " ORDER BY timestamp DESC LIMIT 100"

        result = client_ch.query(query)
        columns = result.column_names
        data = [dict(zip(columns, row)) for row in result.result_rows]

        # Converte datetime para string
        for item in data:
            if hasattr(item["timestamp"], "isoformat"):
                item["timestamp"] = item["timestamp"].isoformat()
            else:
                item["timestamp"] = str(item["timestamp"])

        return data
    except Exception as e:
        print(f"❌ [EXPLORER ERROR] {e}")
        return {"error": str(e)}


@app.get("/api/blacklist")
async def get_blacklist():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="sentinel_vault",
            user="admin",
            password="god_eye_password",
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT ip, reason, created_at FROM blacklist ORDER BY created_at DESC LIMIT 100"
        )
        rows = cur.fetchall()

        blacklist_data = []
        for row in rows:
            blacklist_data.append(
                {
                    "ip": row[0],
                    "reason": row[1],
                    "banned_at": (
                        row[2].isoformat() if row[2] else datetime.now().isoformat()
                    ),
                }
            )

        cur.close()
        conn.close()
        print(f"💀 [SATELLITE] Blacklist extraída: {len(blacklist_data)} hostis.")
        return blacklist_data
    except Exception as e:
        print(f"❌ [DB ERROR] Falha no Postgres: {e}")
        return []


@app.get("/api/intelligence/stats")
async def get_intel_stats():
    try:
        client = get_ch_client()
        # 1. Top IPs
        top_ips = client.query(
            "SELECT ip, count() as total FROM sentinel_logs.events GROUP BY ip ORDER BY total DESC LIMIT 8"
        )

        # 2. Volume de Ataques por último minuto (Gráfico de Pulso)
        pulse = client.query(
            "SELECT toSecond(timestamp) as sec, count() as total FROM sentinel_logs.events WHERE timestamp > now() - INTERVAL 1 MINUTE GROUP BY sec ORDER BY sec"
        )

        # 3. Distribuição de Protocolos
        methods = client.query(
            "SELECT method, count() as total FROM sentinel_logs.events GROUP BY method"
        )

        return {
            "top_ips": [
                dict(zip(top_ips.column_names, row)) for row in top_ips.result_rows
            ],
            "pulse_data": [row[1] for row in pulse.result_rows],
            "methods": [
                dict(zip(methods.column_names, row)) for row in methods.result_rows
            ],
            "threat_level": "DEFCON 2",
            "neural_load": "42.8%",
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/forensics/investigate/{ip}")
async def investigate_target(ip: str):
    print(f"🕵️ [FORENSICS] Iniciando Deep Scan no IP: {ip}")
    try:
        # O motor faz a mágica usando Shodan e AbuseIPDB
        report = forensics_engine.analyze_ip(ip)
        print(f"✅ [FORENSICS] Relatório gerado para {ip}")
        return report
    except Exception as e:
        print(f"❌ [FORENSICS ERROR] Falha na análise de {ip}: {e}")
        return {
            "error": str(e),
            "ip": ip,
            "status": "analysis_failed"
        }
    
@app.get("/api/settings")
async def get_settings():
    # Puxa as configs do Redis ou usa o padrão
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    settings = r.get("sentinel_configs")
    if settings:
        return json.loads(settings)
    return {
        "ban_threshold": 90,
        "challenge_threshold": 40,
        "auto_mitigation": True,
        "debug_mode": False,
        "soc_active": True
    }

@app.post("/api/settings")
async def save_settings(config: dict):
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    r.set("sentinel_configs", json.dumps(config))
    print(f"⚙️ [SETTINGS] Novas diretrizes aplicadas: {config}")
    return {"status": "Updated"}

@app.get("/api/system/health")
async def get_system_health():
    return {
        "cpu_usage": psutil.cpu_percent(),
        "ram_usage": psutil.virtual_memory().percent,
        "kafka_status": "CONNECTED",
        "redis_status": "CONNECTED",
        "uptime": "14d 02h 33m"
    }

@app.get("/api/firewall/check/{ip}")
async def quick_check(ip: str):
    # O Arcanjo central checa no Redis em nanosegundos
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    is_banned = r.sismember("sentinel:arcanjo:blacklist", ip)
    return {"banned": bool(is_banned)}




# --- INSTANCIAÇÃO DOS MOTORES ---
r_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
forensics_engine = OSINTAnalyzer(r_client)

if __name__ == "__main__":
    import uvicorn

    # Roda na porta 8000 (O padrão do Sentinel)
    uvicorn.run(app, host="0.0.0.0", port=8000)
