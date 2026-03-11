package com.sentinel.core.model; // Atenção: mude para o seu package se for diferente!

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;

@Entity
@Table(name = "blacklist")
public class Blacklist {

    @Id
    private String ip;
    
    private String reason;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;

    // --- GETTERS E SETTERS ---
    public String getIp() { return ip; }
    public void setIp(String ip) { this.ip = ip; }
    
    public String getReason() { return reason; }
    public void setReason(String reason) { this.reason = reason; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}