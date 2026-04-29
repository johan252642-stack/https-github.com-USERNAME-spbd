from concurrent.futures import ThreadPoolExecutor

def run_threads(targets, worker):
    results = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        for r in ex.map(worker, targets):
            results.extend(r)
    return results
