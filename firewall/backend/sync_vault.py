import redis
import struct
import time

# Configurações do Sentinel
r = redis.Redis(host='localhost', port=6379, db=0)
VAULT_PATH = "./blacklist.bin"

def update_local_vault():
    print("📡 [SYNC] Sincronizando cofre local com Sentinel Brain...")
    # Pega todos os IPs banidos do Redis
    ips = r.smembers("sentinel:arcanjo:blacklist")
    
    with open(VAULT_PATH, "wb") as f:
        # Escreve o número de IPs (header)
        f.write(struct.pack("I", len(ips)))
        for ip_str in ips:
            try:
                # Converte IP string (1.2.3.4) para 32-bit int
                ip_ints = [int(x) for x in ip_str.split('.')]
                ip_bin = struct.pack("BBBB", *ip_ints)
                f.write(ip_bin)
            except: continue
    print(f"✅ [SYNC] {len(ips)} alvos hostis mapeados no arquivo binário.")

if __name__ == "__main__":
    while True:
        update_local_vault()
        time.sleep(60) # Sincroniza a cada minuto ou via PubSub