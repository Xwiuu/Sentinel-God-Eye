import redis
import json
import subprocess
import os
import ctypes

# Verifica se o script está rodando como Administrador (Necessário para o Firewall)
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

class InfraArcanjo:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.rule_prefix = "SENTINEL_BLOCK_"

    def execute_hard_block(self, ip):
        """Cria uma regra de bloqueio no Firewall do Windows em nível de Kernel"""
        rule_name = f"{self.rule_prefix}{ip}"
        print(f"⚔️ [INFRA] Executando bloqueio de hardware para: {ip}")
        
        # Comando militar: netsh advfirewall
        cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip}'
        
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            print(f"🚫 [TERMINATED] IP {ip} bloqueado no Windows Defender.")
        except Exception as e:
            print(f"❌ Falha ao injetar regra: {e}")

    def listen_for_bans(self):
        """Escuta o canal de rádio do Arcanjo para novos alvos"""
        pubsub = self.r.pubsub()
        pubsub.subscribe("arcanjo:broadcast")
        print("📡 [INFRA] Arcanjo de Infra em escuta ativa... Aguardando ordens.")
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                if data.get('action') == 'DROP':
                    self.execute_hard_block(data['ip'])

if __name__ == "__main__":
    if not is_admin():
        print("🛑 ERRO: O Arcanjo de Infra precisa de privilégios de ADMINISTRADOR.")
    else:
        arcanjo = InfraArcanjo()
        arcanjo.listen_for_bans()