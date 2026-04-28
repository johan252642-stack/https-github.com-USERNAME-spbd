from concurrent.futures import ThreadPoolExecutor

def run_threads(func, items, workers=5):
    results = []

    with ThreadPoolExecutor(max_workers=workers) as exe:
        res = exe.map(func, items)
        for r in res:
            results.append(r)

    return results
