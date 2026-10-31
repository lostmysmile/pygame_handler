# TODO

## Concurrency learning

- [ ] **Foundations:** processes, threads, coroutines, concurrency vs. parallelism, blocking, CPU-bound vs. I/O-bound work, scheduling.
- [ ] **Threading:** `Thread`, lifecycle, daemon threads, `Lock`, `RLock`, `Event`, `Condition`, `Semaphore`, `queue.Queue`, producer-consumer, `ThreadPoolExecutor`, cancellation and shutdown.
- [ ] **Multiprocessing:** `Process`, pools/executors, Windows `spawn`, pickling, `Queue`, `Pipe`, synchronization, shared memory, worker failures and cleanup.
- [ ] **Subprocesses:** `run()`, `Popen()`, command arguments, environment and working directory, stdin/stdout/stderr, pipes, timeouts, termination and process trees.
- [ ] **Running scripts:** imports vs. `runpy` vs. subprocess; launch other Python scripts/interpreters; pass arguments and exchange data.
- [ ] **Asyncio:** coroutines, `async`/`await`, event loop, tasks/futures, `TaskGroup`, `gather()`, `asyncio.Queue`, synchronization, cancellation, timeouts, networking and async subprocesses.
- [ ] **Hybrid concurrency:** combine threads, processes, subprocesses and asyncio; task pipelines, backpressure, communication, error propagation and cancellation.

## Experiments and engineering

- [ ] Build standalone experiments before integrating concurrency into the game.
- [ ] Compare sequential, threaded, process-based and asynchronous implementations.
- [ ] Practise race conditions, deadlocks, blocking, worker crashes and graceful shutdown.
- [ ] Add tests, logging, benchmarks and documentation for each mechanism.

## pygame_handler integration

- [ ] Design a separate concurrency subsystem; keep it independent of scene/event internals.
- [ ] Keep Pygame display, event pumping, rendering and game-state changes on the main thread.
- [ ] Add controlled worker-to-game result communication.
- [ ] Explore threaded asset/file loading and background I/O.
- [ ] Explore process-based procedural generation and CPU-heavy calculations.
- [ ] Explore async networking and multiplayer communication.
- [ ] Integrate task results safely with scenes and entities.
- [ ] Define task ownership, cancellation, error handling and game shutdown.
- [ ] Keep the existing synchronous game loop; consider an explicit async entry point later.

## Advanced applications (after the fundamentals)

- [ ] **Process orchestration:** launch multiple scripts, exchange data, monitor health, restart failures and shut down gracefully.
- [ ] **Mod/plugin support:** load and manage mods, run separate mod scripts where appropriate, define communication protocols and handle failures.
- [ ] **External services:** dedicated servers, simulations and other companion applications.
- [ ] **Development tools:** asset conversion/processing, recording and video conversion, builds and background testing.
- [ ] Evaluate process isolation and security boundaries for untrusted mods; a subprocess alone is not a security sandbox.

## Scope

- [ ] Support standard Python environments.
- [ ] Exclude GIL/free-threaded Python topics from this learning plan.
- [ ] Choose each execution model based on a demonstrated use case; do not build abstractions prematurely.
