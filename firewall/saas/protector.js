// Atualize o topo do seu firewall/saas/protector.js
const SentinelArcanjo = {
    apiHost: "http://localhost:8000",

    async deploy() {
        // Estética Militar no Console
        console.log("%c[!] ARCANJO_SHIELD_DEPLOYED", "color: #00ff41; background: #002200; padding: 5px; font-weight: bold;");
        
        try {
            // Pega seu IP real
            const response = await fetch('https://api.ipify.org?format=json');
            const { ip } = await response.json();
            console.log(`📡 [SHIELD] Analisando Assinatura de IP: ${ip}`);

            // Consulta o seu Satélite Python
            const check = await fetch(`${this.apiHost}/api/firewall/check/${ip}`);
            const { banned } = await check.json();

            if (banned) {
                this.terminateAccess(ip, "IDENTIFIED_HOSTILE");
            } else {
                console.log("%c[+] ARCANJO: Acesso Autorizado.", "color: #00ff41;");
            }
        } catch (e) {
            console.error("⚠️ [SHIELD] Erro de link com Sentinel. Modo preventivo: ALLOW.");
        }
    },

    terminateAccess(ip, status) {
        document.body.innerHTML = `
        <div style="background:#000; color:#ff003c; height:100vh; font-family:monospace; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 10px solid #ff003c; text-transform:uppercase;">
            <h1 style="font-size:4rem; margin:0; font-weight:900;">TERMINATED</h1>
            <p style="background:#ff003c; color:#000; font-weight:bold; padding:2px 10px;">Sentinel Security Protocol Level 3</p>
            <p style="margin-top:20px; letter-spacing:2px;">Hostile activity detected from: ${ip}</p>
            <p style="opacity:0.5; font-size:12px;">Trace ID: ${status}</p>
        </div>`;
        window.stop();
    }
};

SentinelArcanjo.deploy();