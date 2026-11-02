import asyncio
import httpx
import time
import statistics
import matplotlib.pyplot as plt
import urllib3

urllib3.disable_warnings()

URL_HTTP1 = "http://localhost:8000/api/large"
URL_HTTP2 = "https://localhost/api/large"
TOTAL_REQUESTS = 200
CONCURRENCY = 20

async def fetch(client, url):
    start = time.perf_counter()
    try:
        response = await client.get(url)
        end = time.perf_counter()
        return end - start
    except Exception:
        return None

async def run_test(url, use_http2):
    print(f"Запуск теста: {'HTTP/2' if use_http2 else 'HTTP/1.1'}...")
    async with httpx.AsyncClient(http2=use_http2, verify=False) as client:
        await fetch(client, url)
        start_total = time.perf_counter()
        sem = asyncio.Semaphore(CONCURRENCY)
        
        async def sem_fetch():
            async with sem:
                return await fetch(client, url)
                
        tasks = [sem_fetch() for _ in range(TOTAL_REQUESTS)]
        results = await asyncio.gather(*tasks)
        end_total = time.perf_counter()
        
    times = [t for t in results if t is not None]
    total_time = end_total - start_total
    avg_time = statistics.mean(times)
    p95 = statistics.quantiles(times, n=20)[18] if len(times) > 20 else max(times)
    rps = len(times) / total_time
    print(f"Результат: Avg={avg_time:.4f}s, p95={p95:.4f}s, RPS={rps:.1f}")
    return {"avg": avg_time, "p95": p95, "rps": rps}

async def main():
    res1 = await run_test(URL_HTTP1, use_http2=False)
    res2 = await run_test(URL_HTTP2, use_http2=True)
    
    labels = ['HTTP/1.1', 'HTTP/2']
    avg_times = [res1['avg'] * 1000, res2['avg'] * 1000]
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, avg_times, color=['#4C72B0', '#55A868'], width=0.5)
    plt.ylabel('Среднее время отклика (мс)', fontsize=12)
    plt.title('Сравнение времени отклика REST API', fontsize=14)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval:.1f} мс', ha='center', va='bottom', fontsize=12)
        
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('graph_results.png', dpi=300)
    print("График сохранен в файл graph_results.png")

if __name__ == "__main__":
    asyncio.run(main())
