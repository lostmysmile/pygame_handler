
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter, sleep
from threading import get_ident


def pretend_io(task_id: int) -> tuple[int, int]:
    """Simulate an operation waiting for external I/O."""
    
    sleep(1)

    return task_id, get_ident()


def run_sequential(task_count: int):
    results = []

    for task_id in range(task_count):
        results.append(pretend_io(task_id))

    return results


def run_concurrent(task_count: int):
    with ThreadPoolExecutor(max_workers=task_count) as executor:
        results = list(
            executor.map(pretend_io, range(task_count))
        )

    return results


def measure(function, task_count: int):
    started = perf_counter()

    results = function(task_count)

    elapsed = perf_counter() - started

    thread_ids = {thread_id for _, thread_id in results}

    print(f"\nExecution: {function.__name__}")
    print(f"Elapsed: {elapsed:.3f} seconds")
    print(f"Worker threads: {len(thread_ids)}")
    print(f"Results: {results}")


if __name__ == "__main__":
    task_count = 4

    measure(run_sequential, task_count)
    measure(run_concurrent, task_count)
