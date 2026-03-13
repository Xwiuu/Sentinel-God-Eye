import json
import time

class CorrelationEngine:
    def __init__(self, redis_client):
        self.r = redis_client
        self.time_window = 300  # Janela de 5 minutos (300 segundos) para correlação

    def track_and_correlate(self, ip, attacker_id, new_alert_type, severity):
        """
        Guarda o estado do atacante. Se ele ativar múltiplos motores 
        (ex: BotID + Suricata + Wazuh) em menos de 5 minutos, a ameaça escala.
        """
        redis_key = f"killchain:{attacker_id}"
        
        # Vai buscar o histórico do atacante (ou cria um novo)
        history_raw = self.r.get(redis_key)
        if history_raw:
            history = json.loads(history_raw)
        else:
            history = {"ip": ip, "alerts": [], "first_seen": time.time(), "total_score": 0}

        # Adiciona o novo alerta à linha do tempo
        if new_alert_type not in history["alerts"]:
            history["alerts"].append(new_alert_type)
        
        # Calcula a pontuação acumulada
        history["total_score"] += severity

        # Grava de volta no Redis com o tempo de expiração (TTL) de 5 minutos
        self.r.setex(redis_key, self.time_window, json.dumps(history))

        # --- A MAGIA DA CORRELAÇÃO ---
        correlation_msg = None
        is_critical = False

        # Regra 1: Movimentação Lateral / Multi-Vector Attack
        if len(history["alerts"]) >= 3:
            correlation_msg = f"🔥 CORRELAÇÃO CRÍTICA: Ataque Multi-Estágio ({', '.join(history['alerts'])})"
            is_critical = True

        # Regra 2: Bruteforce / Flood de ataques persistentes
        elif history["total_score"] >= 150:
            correlation_msg = "🔥 CORRELAÇÃO CRÍTICA: Persistência Extrema de Ataque"
            is_critical = True

        return is_critical, correlation_msg, history["total_score"]