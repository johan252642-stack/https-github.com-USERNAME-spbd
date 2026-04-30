import concurrent.futures

def run_threads(tasks, func, max_threads=5):
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(func, t) for t in tasks]

        for f in concurrent.futures.as_completed(futures):
            try:
                res = f.result()
                if res:
                    results.extend(res)
            except Exception as e:
                print(f"[ERROR] {e}")

    return results
