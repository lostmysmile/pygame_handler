# TODO — Concurrency & Runtime Engineering

> Learning and implementation roadmap for pygame_handler. Learn mechanisms with standalone experiments first; integrate them only after their trade-offs are understood.

## Scope and principles

- [ ] Use standard Python; exclude GIL/free-threading topics.
- [ ] Learn on Windows first, then check platform differences on Linux/macOS.
- [ ] Prefer explicit ownership and message passing over shared mutable state.
- [ ] Keep Pygame's display, event pump, rendering and live scene/entity mutation on the main thread.
- [ ] Prefer high-level APIs by default; understand lower-level APIs before building abstractions.
- [ ] Give every worker, task, queue and process a defined owner and shutdown path.
- [ ] Bound work and resources; more workers do not automatically mean better performance.

## Phase 1 — Operating-system and concurrency foundations

- [ ] Processes, threads, address spaces, stacks, handles, scheduling and context switches.
- [ ] Coroutines, event loops, executors, futures and cooperative scheduling.
- [ ] Concurrency vs. parallelism; preemptive vs. cooperative execution.
- [ ] Blocking vs. non-blocking; synchronous vs. asynchronous APIs.
- [ ] CPU-bound vs. I/O-bound workloads; latency vs. throughput.
- [ ] Shared memory vs. message passing; isolation and communication costs.
- [ ] Timeouts, monotonic clocks, deadlines, timers and time budgets.
- [ ] Resource limits: CPU, memory, threads, processes, file descriptors and OS handles.

## Phase 2 — Threading

### Thread lifecycle and management

- [ ] Thread: target, args, kwargs, start, run, join, is_alive, name and identifiers.
- [ ] Daemon vs. non-daemon threads; current_thread, main_thread, active_count and enumerate.
- [ ] Worker exceptions, threading.excepthook, cooperative stop flags and cleanup.
- [ ] Timer, local thread-local storage, stack_size and Barrier.

### Synchronization primitives — study each explicitly

- [ ] threading.Lock: mutual exclusion, context manager, blocking, non-blocking and timeout acquisition.
- [ ] threading.RLock: reentrancy, ownership, recursion count and nested calls.
- [ ] threading.Event: set, clear, is_set, wait, timeouts and stop signaling.
- [ ] threading.Condition: associated lock, wait, wait_for, notify, notify_all and predicate loops.
- [ ] threading.Semaphore: counter, permits, bounded resource access and correct acquire/release pairing.
- [ ] threading.BoundedSemaphore: over-release detection and resource-capacity protection.
- [ ] threading.Barrier: parties, wait, action, timeout, broken state, reset and reusable phases.
- [ ] Primitive selection, lock scope, lock ordering and avoiding nested-lock problems.

### Thread communication and task execution

- [ ] queue.Queue, SimpleQueue, LifoQueue, PriorityQueue, Empty, Full and bounded queues.
- [ ] Queue task tracking: task_done, join, shutdown and ShutDown (Python 3.13+).
- [ ] ThreadPoolExecutor: submit, map, worker initialization, context management and shutdown.
- [ ] Future: states, result, exception, done, running, cancel, callbacks and timeouts.
- [ ] wait, as_completed, result ordering and exception propagation.
- [ ] Thread naming, context propagation, thread-safe logging and debugging.
- [ ] Common mistakes: shared mutable state, holding locks during I/O, blocking joins and executor self-deadlocks.

## Phase 3 — Thread-safe data structures and coordination patterns

- [ ] FIFO, LIFO, priority and bounded work queues; task queues vs. message queues.
- [ ] Producer-consumer, multi-producer/multi-consumer and work-dispatcher structures.
- [ ] Shared dictionaries/lists protected by locks; immutable messages and snapshot/copy-on-write approaches.
- [ ] Thread-local state, ownership-based state and message-passing designs.
- [ ] Mailboxes, channels, event bus and publish-subscribe patterns.
- [ ] Actor model and one-owner-per-state designs.
- [ ] Reader-writer locks, read-mostly data and lock striping (concepts and trade-offs; not built into threading).
- [ ] Ring buffers, bounded buffers and concurrent iterator limitations.
- [ ] Lock-free/non-blocking concepts, atomicity limits and when not to implement custom primitives.
- [ ] Compare standard-library structures with carefully selected third-party options.

## Phase 4 — concurrent.futures and executor design

- [ ] Executor abstraction and differences between ThreadPoolExecutor and ProcessPoolExecutor.
- [ ] Future lifecycle, callbacks, cancellation limits and exception retrieval.
- [ ] submit vs. map; wait vs. as_completed; ordering and batching.
- [ ] Worker count, queueing, task granularity, backpressure and executor reuse.
- [ ] Nested executor calls, deadlocks, starvation and shutdown semantics.
- [ ] Distinguish concurrent.futures.Future from asyncio.Future.

## Phase 5 — Multiprocessing

### Processes and start contexts

- [ ] Process: target, args, name, daemon, start, join, exitcode, is_alive and close.
- [ ] terminate, kill, sentinels and why forced termination can corrupt shared resources.
- [ ] spawn, fork, forkserver, platform defaults and get_context.
- [ ] Windows main guard, import-safe entry points and freeze_support.
- [ ] Pickling, importability, serialization overhead and safe task boundaries.

### IPC, shared data and synchronization

- [ ] multiprocessing.Queue, SimpleQueue, JoinableQueue, Pipe and Connection.
- [ ] multiprocessing.Lock, RLock, Event, Condition, Semaphore, BoundedSemaphore and Barrier.
- [ ] Manager, proxies, manager queues/dicts/lists and their performance costs.
- [ ] Value, Array, shared ctypes and shared_memory.
- [ ] Resource tracking, shared-memory ownership, closing and unlinking.
- [ ] Message ordering, queue feeder threads, pipe safety, draining queues and joining workers.

### Pools and failure handling

- [ ] Pool: map, starmap, imap, async results, callbacks, initializer and maxtasksperchild.
- [ ] ProcessPoolExecutor: mp_context, initializer, chunking and worker limits.
- [ ] Worker crashes, BrokenProcessPool, timeouts, retries and pool recreation.
- [ ] Avoid unnecessary data copying and large IPC payloads; benchmark serialization costs.

## Phase 6 — Subprocesses and running other scripts

- [ ] Execution choices: imports, runpy, python script.py, python -m, console entry points and subprocesses.
- [ ] subprocess.run, Popen, CompletedProcess, poll, wait, communicate and return codes.
- [ ] Select interpreters with sys.executable; launch another venv or executable intentionally.
- [ ] Arguments, cwd, env, executable lookup, encoding and working-directory rules.
- [ ] stdin/stdout/stderr, pipes, streaming output, buffering and pipe deadlocks.
- [ ] Timeouts, terminate/kill, signal handling, process groups/trees and Windows process details.
- [ ] shell=True risks, argument-list usage, quoting and untrusted input.
- [ ] Child process readiness, health checks, structured messages and continuous communication.
- [ ] Parent/child crash behaviour, inherited handles, orphan processes and cleanup.

## Phase 7 — Asyncio

### Runtime and task model

- [ ] Coroutine functions, coroutine objects, awaitables, event loop, Task and Future.
- [ ] async, await, suspension points, cooperative scheduling and event-loop blocking.
- [ ] asyncio.run, task creation/naming, loop callbacks and task inspection.
- [ ] TaskGroup and structured concurrency; gather, wait and as_completed.
- [ ] ExceptionGroup, exception propagation and task lifetime/ownership.
- [ ] Cancellation, CancelledError, try/finally, shielding and cancellation propagation.
- [ ] timeout, timeout_at, deadlines and cleanup on cancellation.

### Async synchronization and communication

- [ ] asyncio.Lock, Event, Condition, Semaphore and BoundedSemaphore.
- [ ] asyncio.Queue, PriorityQueue, LifoQueue, bounded queues and task tracking.
- [ ] Async producer-consumer, workers, fan-out/fan-in and backpressure.
- [ ] Async primitives are not thread-safe; understand cross-thread handoff.

### I/O, networking and integration

- [ ] Streams, readers/writers, sockets, protocols/transports and async context managers.
- [ ] Async iterators/generators and deterministic async-generator cleanup.
- [ ] TCP/UDP, client/server patterns, reconnects, timeouts and connection limits.
- [ ] asyncio.to_thread, run_in_executor, process pools and run_coroutine_threadsafe.
- [ ] call_soon_threadsafe, loop ownership and cross-thread communication.
- [ ] Async subprocess creation, stream reading, termination and cleanup.
- [ ] Debug mode, slow callbacks, un-awaited coroutines and unhandled task exceptions.

## Phase 8 — Architecture and reusable concurrency patterns

- [ ] Producer-consumer, worker pool, pipeline, fan-out/fan-in, fork-join and map-reduce.
- [ ] Task graphs/DAGs, dependencies, task schedulers and priority scheduling.
- [ ] Actor, message bus, pub-sub, request-response and command queue.
- [ ] Work stealing and work sharing; understand pool scheduling trade-offs.
- [ ] Bounded queues, backpressure, batching, rate limiting and load shedding.
- [ ] Token bucket/leaky bucket rate limiters and concurrency bulkheads.
- [ ] Resource pools, connection pools and bounded permits.
- [ ] Reader-writer patterns, immutable snapshots, copy-on-write and lock striping.
- [ ] Structured concurrency, task scopes, supervision trees and explicit ownership.
- [ ] State machines for task/process states: pending, running, stopping, succeeded, failed and cancelled.
- [ ] Retry policies, exponential backoff, jitter, idempotency and duplicate-work protection.
- [ ] Circuit breakers, watchdogs, heartbeats, health checks and restart policies.
- [ ] Ordering, delivery guarantees, acknowledgement, correlation IDs and deduplication.
- [ ] Distributed-systems basics: RPC, message brokers, serialization formats and network failure.

## Phase 9 — Reliability, safety and operational engineering

- [ ] Deadlock, livelock, starvation, priority inversion, contention and race diagnosis.
- [ ] Lock hierarchy, consistent lock ordering, short critical sections and timeouts.
- [ ] Avoid polling and unreliable queue empty/qsize checks for coordination.
- [ ] Cooperative cancellation, sentinel messages, graceful shutdown and shutdown ordering.
- [ ] Failure containment, worker supervision, restart limits and failure escalation.
- [ ] Resource budgets, bounded work submission and overload behaviour.
- [ ] Safe serialization; never unpickle untrusted data.
- [ ] Secure subprocess invocation; least privilege and explicit environment configuration.
- [ ] Process isolation is not a complete security sandbox; investigate OS-level isolation for untrusted code.
- [ ] Logging, metrics, tracing/correlation IDs and actionable error reporting.
- [ ] QueueHandler/QueueListener for centralized multi-thread/process logging.
- [ ] Configuration, feature flags, diagnostics and operational controls.

## Phase 10 — Testing, debugging and performance

- [ ] Deterministic tests using Events, Conditions and Barriers instead of timing-only sleeps.
- [ ] Stress, soak, race, fault-injection and shutdown-under-load tests.
- [ ] Test timeouts, worker crashes, queue saturation, cancellation and resource leaks.
- [ ] Capture worker exceptions; test error propagation and recovery.
- [ ] Logging with process/thread/task names and correlation IDs.
- [ ] Diagnose hangs, deadlocks, blocked queues, orphan processes and leaked handles.
- [ ] Benchmark against sequential baselines; measure latency, throughput and variance.
- [ ] Profile CPU, memory, context switches, serialization and IPC overhead.
- [ ] Tune worker count, task size, queue capacity and batching; avoid oversubscription.
- [ ] Measure frame-time impact, not just total task completion time.

## Phase 11 — Pygame integration

- [ ] Keep display creation/use, event pumping and rendering on the main thread.
- [ ] Workers receive plain data; do not share live Game, Scene, entity or display objects.
- [ ] Build a thread-safe result/error/progress inbox consumed by the game loop.
- [ ] Bound result processing per frame to prevent completion bursts causing frame hitches.
- [ ] Threaded file I/O and asset-loading pipeline; safely hand off data for main-thread Pygame object creation/conversion where required.
- [ ] Process-based procedural generation, pathfinding experiments and heavy calculations.
- [ ] Async networking, multiplayer communication and reconnect handling.
- [ ] Scene-owned vs. game-owned tasks; cancel or invalidate results when a scene changes.
- [ ] Stale-result protection with task IDs/generation tokens.
- [ ] Define task priorities, progress reporting, cancellation and error callbacks.
- [ ] Preserve synchronous Game.run; evaluate an explicit async entry point separately.
- [ ] Define game shutdown order and ensure all owned workers/processes are cleaned up.

## Phase 12 — Advanced applications

- [ ] Script runner: launch scripts, select interpreters/venvs, pass arguments and collect results.
- [ ] Process orchestration: multiple scripts, IPC, health monitoring, restart policies and graceful shutdown.
- [ ] Mod/plugin architecture: in-process vs. subprocess plugins, API boundaries, protocols and lifecycle.
- [ ] Mod security: permissions, trust model and OS-level isolation; subprocess alone is not a sandbox.
- [ ] Dedicated game servers, external simulations and companion applications.
- [ ] Asset pipelines, image/audio processing, FFmpeg recording/conversion, builds and background testing.

## Phase 13 — Professional library engineering and conventions

- [ ] Public API design: explicit contracts, predictable errors, type hints, generics and documented thread-safety guarantees.
- [ ] Keep executor-specific semantics visible; do not force threads, processes, subprocesses and asyncio into a misleading common abstraction.
- [ ] Context managers for ownership; avoid hidden global executors and unmanaged background workers.
- [ ] Naming, docstrings, type checking, linting, formatting and import hygiene.
- [ ] PEP 8/257 style; PEP 484 typing; pyproject.toml packaging conventions.
- [ ] Version policy: PEP 440-compliant releases; document compatibility and deprecations.
- [ ] Semantic versioning as a release-policy concept where appropriate; distinguish it from Python version-specifier rules.
- [ ] Test public API contracts, supported Python versions and Windows/Linux behaviour in CI.
- [ ] Document thread/process safety, blocking behaviour, cancellation guarantees and shutdown requirements.
- [ ] Provide runnable examples, architecture diagrams, sequence diagrams and troubleshooting guides.
- [ ] Review dependencies, licenses, maintenance status and security implications before adoption.
- [ ] Maintain changelog, migration notes and backwards-compatibility policy.

## Phase 14 — pygame_handler implementation deliverables

- [ ] Write an architecture decision record (ADR) for each major concurrency decision.
- [ ] Create independent examples and benchmarks before production modules.
- [ ] Design task handles, status, results, exceptions, progress and cancellation contracts.
- [ ] Design distinct thread, process, subprocess and async managers with explicit ownership.
- [ ] Define message/result schemas and queue capacity policies.
- [ ] Add unit, integration, stress and platform-specific tests.
- [ ] Add examples, API documentation, diagrams and troubleshooting notes.
- [ ] Avoid premature abstractions; every feature needs a demonstrated use case.

## References

- [Python concurrent execution overview](https://docs.python.org/3/library/concurrency.html)
- [threading](https://docs.python.org/3/library/threading.html)
- [queue](https://docs.python.org/3/library/queue.html)
- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [subprocess](https://docs.python.org/3/library/subprocess.html)
- [asyncio](https://docs.python.org/3/library/asyncio.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [QueueHandler and QueueListener](https://docs.python.org/3/library/logging.handlers.html)
- [Python Packaging User Guide](https://packaging.python.org/)
- [pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- [PEP 8 — Style Guide](https://peps.python.org/pep-0008/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [PEP 440 — Version Identification](https://peps.python.org/pep-0440/)
- [Pygame documentation](https://www.pygame.org/docs/)
