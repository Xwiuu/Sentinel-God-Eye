// SENTINEL CHIP V0.1 - O Olho que tudo vê
const Sentinel = {
    config: {
        endpoint: "http://localhost:8080/ingest",
        project: "MEU_PROJETO_TESTE"
    },

    init(projectName) {
        this.config.project = projectName;
        console.log("👁️ SENTINEL Ativado em: " + projectName);
        this.trackVisit();
    },

    async trackVisit() {
        const payload = {
            project: this.config.project,
            path: window.location.pathname + window.location.search,
            user_agent: navigator.userAgent
        };

        try {
            const response = await fetch(this.config.endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            console.log("📡 Sentinel Response:", data.eye); // Deve retornar "observing"
        } catch (error) {
            console.error("⚠️ Sentinel Offline");
        }

        // sentinel-chip.js (Parte do fetch)
        const response = await fetch(this.config.endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Sentinel-Token": "god-eye-2026" // O NOVO ESCUDO
            },
            body: JSON.stringify(payload)
        });
    }
};

// Exemplo de uso imediato:
Sentinel.init("MINHA_SOFTWARE_HOUSE");