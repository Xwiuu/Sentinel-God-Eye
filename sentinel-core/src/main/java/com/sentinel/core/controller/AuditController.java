package com.sentinel.core.controller;

import com.sentinel.core.model.Blacklist;
import com.sentinel.core.model.Event; // O IMPORT QUE FALTAVA
import com.sentinel.core.repository.BlacklistRepository;
import com.sentinel.core.repository.EventRepository; // O OUTRO IMPORT QUE FALTAVA
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/audit")
@CrossOrigin(origins = "*")
public class AuditController {

    @Autowired
    private BlacklistRepository blacklistRepository;

    @Autowired
    private EventRepository eventRepository; // Injetando o novo repositório

    // Endpoint do Cemitério (Banidos)
    @GetMapping("/blacklist")
    public List<Blacklist> getBannedHackers() {
        return blacklistRepository.findAllByOrderByCreatedAtDesc();
    }

    // Endpoint do Olho que Tudo Vê (Tráfego em Tempo Real)
    @GetMapping("/live-traffic")
    public List<Event> getLiveTraffic() {
        System.out.println("👁️ [GOD EYE] Capturando tráfego em tempo real para o Dashboard...");
        return eventRepository.findTop50ByOrderByTimestampDesc();
    }
}