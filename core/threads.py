from concurrent.futures import ThreadPoolExecutor, as_completed

def run_threads(targets, worker, max_threads=10):
    results = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(worker, t) for t in targets]

        for f in as_completed(futures):
            try:
                results.extend(f.result())
            except:
                pass

    return results
