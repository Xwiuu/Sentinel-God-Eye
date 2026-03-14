package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"log"
	"sync"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	_ "github.com/lib/pq"
	"github.com/segmentio/kafka-go"
)

var (
	db             *sql.DB
	blacklistCache sync.Map
	kafkaWriter    *kafka.Writer
)

// A nova estrutura do Evento
type SentinelEvent struct {
	IP          string            `json:"ip"`
	Method      string            `json:"method"`
	Path        string            `json:"path"`
	Headers     map[string]string `json:"headers"`
	Body        string            `json:"body"`
	UserAgent   string            `json:"user_agent"`
	Timestamp   string            `json:"timestamp"`
}

func initDB() {
	// Mantemos o Postgres APENAS para ler a Blacklist oficial (O Cemitério)
	connStr := "host=localhost port=5432 user=admin password=god_eye_password dbname=sentinel_vault sslmode=disable"
	var err error
	db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("ERRO DB: ", err)
	}
}

func housekeeper() {
	// Atualiza o cache de banimentos na RAM a cada 1 minuto
	for {
		rows, err := db.Query("SELECT ip FROM blacklist")
		if err == nil {
			for rows.Next() {
				var ip string
				rows.Scan(&ip)
				blacklistCache.Store(ip, true)
			}
			rows.Close()
		}
		time.Sleep(1 * time.Minute)
	}
}

func initKafka() {
	// Conecta no Redpanda (Kafka) que subimos no Docker
	kafkaWriter = &kafka.Writer{
		Addr:     kafka.TCP("localhost:19092"),
		Topic:    "sentinel-live-traffic", // O "Cano" de dados
		Balancer: &kafka.LeastBytes{},
	}
}

func main() {
	initDB()
	initKafka()
	go housekeeper()

	app := fiber.New(fiber.Config{
		DisableStartupMessage: true, // Modo silencioso e rápido
	})
	app.Use(cors.New())

	// Endpoint para o Python avisar o Go de um banimento instantâneo
	app.Post("/sync-ban", func(c *fiber.Ctx) error {
		var req struct {
			IP string `json:"ip"`
		}
		if err := c.BodyParser(&req); err == nil {
			blacklistCache.Store(req.IP, true)
		}
		return c.SendStatus(200)
	})

	// O ASPIRADOR DE ALTA PERFORMANCE
	app.All("/ingest", func(c *fiber.Ctx) error {
		ip := c.IP()

		// Verifica na RAM se o cara já tá banido (Latência zero)
		if _, banned := blacklistCache.Load(ip); banned {
			return c.Status(403).SendString("SENTINEL_BLOCK: TERMINATED")
		}

		event := SentinelEvent{
			IP:        ip,
			Method:    c.Method(),
			Path:      c.OriginalURL(),
			UserAgent: c.Get("User-Agent"),
			Body:      string(c.Body()),
			Timestamp: time.Now().UTC().Format(time.RFC3339),
			Headers:   make(map[string]string),
		}

		c.Request().Header.VisitAll(func(key, value []byte) {
			event.Headers[string(key)] = string(value)
		})

		// Empacota em JSON
		eventJSON, _ := json.Marshal(event)
		
		// Atira no Kafka em uma Goroutine separada (não trava a requisição)
		go func() {
			err := kafkaWriter.WriteMessages(context.Background(),
				kafka.Message{
					Key:   []byte(ip), // Usamos o IP como chave para o Kafka organizar a fila
					Value: eventJSON,
				},
			)
			if err != nil {
				log.Println("⚠️ Erro ao enviar pro Kafka:", err)
			}
		}()

		return c.Status(202).JSON(fiber.Map{"status": "captured"})
	})

	log.Println("📥 [SENSOR] Pacote processado e enviado ao Redpanda")
	log.Fatal(app.Listen(":8080"))
}