package com.sentinel.core.repository;

import com.sentinel.core.model.Blacklist;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BlacklistRepository extends JpaRepository<Blacklist, String> {
    
    // O Java lê esse nome e traduz para: SELECT * FROM blacklist ORDER BY created_at DESC
    List<Blacklist> findAllByOrderByCreatedAtDesc();
}