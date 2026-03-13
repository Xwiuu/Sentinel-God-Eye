import subprocess
import threading
import os
import shutil
import requests
import json

class SOCOrchestrator:
    def __init__(self):
        # Diretórios de Perícia (Forensics)
        self.pcap_dir = "./forensics/pcaps"
        self.nmap_dir = "./forensics/scans"
        self.vuln_dir = "./forensics/reports"
        os.makedirs(self.pcap_dir, exist_ok=True)
        os.makedirs(self.nmap_dir, exist_ok=True)
        os.makedirs(self.vuln_dir, exist_ok=True)

        # Configurações de APIs (SIEM e Threat Intel)
        self.misp_url = "https://misp.local/attributes/restSearch"
        self.misp_key = "SUA_CHAVE_MISP"
        self.wazuh_api = "https://wazuh-manager.local:55000"
        self.wazuh_token = "SEU_TOKEN_WAZUH"
        self.security_onion_elastic = "https://security-onion.local:9200" # Onde ficam logs do Suricata/Zeek

    # ==========================================
    # ⚔️ ARMAS ATIVAS (CONTRA-ATAQUE & PERÍCIA)
    # ==========================================

    def trigger_wireshark(self, ip, duration=60):
        """[Ferramenta 1] WIRESHARK / TSHARK: Grava os pacotes de rede do ataque"""
        # Procura no PATH do sistema, ou vai direto na pasta padrão do Windows
        tshark_path = shutil.which("tshark")
        if not tshark_path and os.path.exists(r"C:\Program Files\Wireshark\tshark.exe"):
            tshark_path = r'"C:\Program Files\Wireshark\tshark.exe"'
            
        if not tshark_path:
            print("⚠️ [WIRESHARK] TShark não instalado ou não encontrado. Pulando PCAP.")
            return

        pcap_file = f"{self.pcap_dir}/attack_{ip}.pcap"
        print(f"🦈 [WIRESHARK] Gravando PCAP forense do IP {ip}...")
        
        def run_capture():
            # TShark escutando a interface 1 (padrão do Windows) em vez de 'any'
            cmd = f'{tshark_path} -i 1 -Y "ip.addr == {ip}" -a duration:{duration} -w {pcap_file}'
            try:
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(pcap_file): 
                    print(f"📁 [FORENSE] PCAP salvo: {pcap_file}")
            except Exception as e: 
                print(f"⚠️ [WIRESHARK ERRO]: {e}")

        threading.Thread(target=run_capture, daemon=True).start()

    def trigger_nmap(self, ip):
        """[Ferramenta 2] NMAP: Counter-Scan para mapear a máquina do atacante"""
        # Procura no PATH do sistema, ou vai direto na pasta padrão do Windows
        nmap_path = shutil.which("nmap")
        if not nmap_path and os.path.exists(r"C:\Program Files (x86)\Nmap\nmap.exe"):
            nmap_path = r'"C:\Program Files (x86)\Nmap\nmap.exe"'
            
        if not nmap_path:
            print("⚠️ [NMAP] Nmap não instalado ou não encontrado. Pulando Counter-Scan.")
            return

        scan_file = f"{self.nmap_dir}/nmap_{ip}.txt"
        print(f"🎯 [NMAP] Iniciando Counter-Scan no IP {ip}...")
        
        def run_nmap():
            cmd = f'{nmap_path} -Pn -F -O {ip}' 
            try:
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if res.stdout:
                    with open(scan_file, "w") as f: 
                        f.write(res.stdout)
                    print(f"🗺️ [INTEL] Counter-Scan concluído para {ip}")
            except Exception as e: 
                print(f"⚠️ [NMAP ERRO]: {e}")

        threading.Thread(target=run_nmap, daemon=True).start()

    def trigger_openvas(self, ip):
        """[Ferramenta 3] OPENVAS: Caça vulnerabilidades no servidor do hacker"""
        gvm_path = shutil.which("gvm-cli")
        if not gvm_path:
            print("⚠️ [OPENVAS] Greenbone/OpenVAS não instalado. Pulando Scan de Vulnerabilidade.")
            return

        print(f"☢️ [OPENVAS] Varredura profunda iniciada contra {ip}...")
        def run_openvas():
            cmd = f'gvm-cli socket --xml "<create_task><name>Sentinel_{ip}</name><target id=\'{ip}\'/></create_task>"'
            try:
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"☢️ [OPENVAS] Task criada no painel Greenbone para {ip}")
            except Exception as e: 
                print(f"⚠️ [OPENVAS ERRO]: {e}")

        threading.Thread(target=run_openvas, daemon=True).start()

    def trigger_metasploit(self, ip):
        """[Ferramenta 4] METASPLOIT: Sondagem ofensiva (Red Team Automatizado)"""
        # Adicionado verificação de caminho padrão caso você instale no Windows futuramente
        msf_path = shutil.which("msfconsole")
        if not msf_path and os.path.exists(r"C:\metasploit-framework\bin\msfconsole.bat"):
            msf_path = r'"C:\metasploit-framework\bin\msfconsole.bat"'

        if not msf_path:
            print("⚠️ [METASPLOIT] MSFConsole não instalado. Pulando sondagem armada.")
            return

        print(f"💀 [METASPLOIT] Acionando sondagem ofensiva contra {ip}...")
        def run_msf():
            cmd = f'{msf_path} -q -x "use auxiliary/scanner/portscan/tcp; set RHOSTS {ip}; run; exit"'
            try:
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"💀 [METASPLOIT] Sondagem concluída contra {ip}.")
            except Exception as e: 
                print(f"⚠️ [METASPLOIT ERRO]: {e}")

        threading.Thread(target=run_msf, daemon=True).start()

    # ==========================================
    # 📡 ANTENAS DE INTELIGÊNCIA (APIs & SIEM)
    # ==========================================

    def query_misp(self, ip):
        """[Ferramenta 5] MISP: Verifica se o IP é um criminoso procurado globalmente"""
        headers = {"Authorization": self.misp_key, "Accept": "application/json", "Content-Type": "application/json"}
        try:
            # Em produção, usa requests.post() aqui. Retornando falso provisório para não travar seu teste local.
            # res = requests.post(self.misp_url, headers=headers, json={"value": ip, "type": "ip-src"}, timeout=2)
            # if res.status_code == 200 and len(res.json().get("response", {}).get("Attribute", [])) > 0:
            #     return True, "MISP ALERT: IP listado em feeds de Threat Intel!"
            return False, ""
        except: return False, ""

    def query_wazuh(self, ip):
        """[Ferramenta 6] WAZUH: Verifica se o atacante já tentou invadir o Linux via SSH/Arquivos"""
        headers = {"Authorization": f"Bearer {self.wazuh_token}"}
        try:
            # Consulta a API do Wazuh para ver se o IP acionou regras de Host-Based IDS
            # res = requests.get(f"{self.wazuh_api}/security/alerts?srcip={ip}", headers=headers, timeout=2)
            return False, ""
        except: return False, ""

    def query_security_onion(self, ip):
        """[Ferramentas 7, 8 e 9] SURICATA, ZEEK e SECURITY ONION: Busca no ElasticSearch do Onion"""
        # Security Onion junta os logs do Suricata (IDS de Rede) e Zeek (Metadados de Rede) no ElasticSearch.
        try:
            # query = {"query": {"match": {"source_ip": ip}}}
            # res = requests.post(f"{self.security_onion_elastic}/_search", json=query, timeout=2)
            # if res.status_code == 200 and res.json()['hits']['total']['value'] > 0:
            #     return True, "SECURITY ONION: Suricata/Zeek detectaram tráfego hostil prévio deste IP."
            return False, ""
        except: return False, ""

    # ==========================================
    # 🧠 EXECUÇÃO TOTAL (O BOTÃO VERMELHO)
    # ==========================================
    def execute_full_soc_response(self, ip):
        """Dispara todas as armas simultaneamente contra o alvo"""
        print(f"\n🚀 [SOC ORCHESTRATOR] INICIANDO PROTOCOLO DE DEFESA TOTAL NÍVEL MILITAR CONTRA {ip}...")
        self.trigger_wireshark(ip)
        self.trigger_nmap(ip)
        self.trigger_openvas(ip)
        self.trigger_metasploit(ip)
        print("🛡️ [SOC ORCHESTRATOR] Orquestração concluída em background.\n")