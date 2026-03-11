package com.sentinel.core.repository;

import com.sentinel.core.model.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface EventRepository extends JpaRepository<Event, Long> {
    // Pega as últimas 50 requisições que entraram no sistema
    List<Event> findTop50ByOrderByTimestampDesc();
}