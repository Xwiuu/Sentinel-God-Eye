package com.sentinel.core.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "events")
public class Event {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String ip;
    private String method;
    private String path;
    private String host;
    private Integer threatScore;
    private LocalDateTime timestamp;

    // Getters e Setters (ou use @Data do Lombok)
    public String getIp() { return ip; }
    public String getMethod() { return method; }
    public String getPath() { return path; }
    public Integer getThreatScore() { return threatScore; }
    public LocalDateTime getTimestamp() { return timestamp; }
}