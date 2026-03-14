// Gatekeeper.js - Coloque no rodapé das suas LPs
(function() {
    // Cria um link invisível para humanos, mas irresistível para BOTS
    const honey = document.createElement('a');
    honey.href = "/admin-login-portal"; 
    honey.style.display = 'none';
    honey.id = 'sentinel-trap';
    document.body.appendChild(honey);

    honey.addEventListener('click', async (e) => {
        e.preventDefault();
        console.error("🚨 HONEYPOT TRIGGERED! SIGNALING SENTINEL...");
        
        // Reporta pro Brain banir esse IP imediatamente
        const clientIp = await fetch('https://api.ipify.org?format=json').then(r => r.json());
        await fetch(`http://localhost:8000/api/report/honeypot`, {
            method: 'POST',
            body: JSON.stringify({ ip: clientIp.ip, reason: "Honeypot Trap: LP Scraper" })
        });

        alert("CRITICAL_SYSTEM_ERROR: Your IP has been flagged.");
        window.location.href = "about:blank";
    });
})();