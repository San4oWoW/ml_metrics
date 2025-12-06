# Настройка алертинга в Grafana при нарушении SLO

## Описание

Репозиторий содержит простой демонстрационный сервис на Python, который экспортирует
метрики в формате Prometheus и используется для настройки мониторинга и алертинга
в Grafana.


## SLO

- **Метрика:** `request_latency_seconds` (Prometheus Histogram)
- **Показатель:** p95 latency
- **SLO:** p95 latency `< 1` секунды на окне 5 минут

При превышении p95 латентности выше 1 секунды алерт `HighLatency` должен
переходить в состояние `Pending`, а затем `Firing`.


## Структура репозитория

```text
.
├── app.py
├── requirements.txt
├── docker-compose.yml
├── prometheus/
│   └── prometheus.yml
├── grafana-dashboard-ml-slo.json
└── screenshots/
    ├── dashboard_p95_latency.png
    ├── alert_rules_pending_or_firing.png
    └── notification.png
```


## Запуск

### Python

```bash
pip install -r requirements.txt
python app.py
```

Медленный режим:

```bash
SLOW_MODE=1 python app.py
```

### Prometheus + Grafana

```bash
docker compose up -d
```

Prometheus: http://localhost:9090  
Grafana: http://localhost:3000

## Настройка Grafana

### Запрос p95 latency

```promql
histogram_quantile(
  0.95,
  sum(rate(request_latency_seconds_bucket[5m])) by (le)
)
```

### Alert rule

```
WHEN QUERY IS ABOVE 1
```

Pending period: 1–2 минуты  
Evaluation interval: 1–2 минуты

## Проверка алерта

1. Запускаем сервис в обычном режиме — p95 < 1s, алерт Normal.
2. Запускаем с `SLOW_MODE=1` — p95 > 1s → Pending → Firing.


## Скриншоты

Папка `screenshots/` содержит:

- график p95 latency,
- состояние алерта (Pending/Firing)
