# REST API HTTP/1.1 vs HTTP/2 Benchmark

Сравнительный анализ производительности REST API при использовании различных протоколов передачи гипертекста (HTTP/1.1 и HTTP/2).

## Стек технологий
* **Python 3.11 / FastAPI** (ASGI)
* **Uvicorn** (ASGI-сервер)
* **Docker / Docker Compose**
* **Nginx** (reverse proxy, TLS, HTTP/2)

## Архитектура
1. **FastAPI** разворачивается в Docker-контейнере (порт 8000).
2. **Nginx** разворачивается перед FastAPI, принимает HTTPS + HTTP/2 (порт 443) и проксирует запросы по HTTP/1.1.
3. **Python-скрипт (benchmark.py)** генерирует нагрузку на оба эндпоинта, замеряет задержки и пропускную способность (RPS), после чего строит график.

## Как запустить
 ` ash
docker compose up -d --build
 ` 

### Запуск бенчмарка
 ` ash
python -m pip install httpx[http2] matplotlib
python benchmark.py
 ` 

## Результаты
Результаты замеров и построенный график сохраняются в файл graph_results.png.