import redis
import json

class ArcanjoCore:
    def __init__(self):
        # Conexão de ultra velocidade para decisões em tempo real
        self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.blacklist_key = "sentinel:arcanjo:blacklist"

    def is_terminated(self, ip):
        """Consulta rápida: 1 se estiver banido, 0 se estiver limpo"""
        return self.r.sismember(self.blacklist_key, ip)

    def sync_from_brain(self, ip, reason):
        """O Brain chama isso para atualizar todos os Arcanjos"""
        self.r.sadd(self.blacklist_key, ip)
        # Opcional: Publica um evento para firewalls que usam hooks
        self.r.publish("arcanjo:broadcast", json.dumps({"action": "DROP", "ip": ip, "reason": reason}))
        print(f"⚔️ [ARCANJO] Alvo {ip} adicionado à lista de execução global.")

    def pardon_ip(self, ip):
        """Remove o IP da lista de morte"""
        self.r.srem(self.blacklist_key, ip)
        print(f"🕊️ [ARCANJO] Alvo {ip} recebeu perdão operacional.")