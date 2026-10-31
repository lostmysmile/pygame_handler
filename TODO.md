# TODO

## Learning scope

- [ ] Use standard Python; exclude GIL/free-threading topics.
- [ ] Build standalone experiments before adding production abstractions.
- [ ] Test on Windows and another supported platform where practical.

## Phase 1 — Foundations

- [ ] **OS basics:** process/thread lifecycle, address spaces, stacks, handles, scheduling and context switches.
- [ ] **Execution models:** threads, processes, coroutines, executors, futures and event loops.
- [ ] **Core distinctions:** concurrency vs. parallelism; cooperative vs. preemptive scheduling; blocking vs. non-blocking; CPU-bound vs. I/O-bound.
- [ ] **Performance:** latency, throughput, resource costs, timers, monotonic clocks and deadlines.
- [ ] **Correctness:** shared state, critical sections, atomicity, race conditions, thread safety, deadlocks, livelocks and starvation.
- [ ] **Coordination styles:** shared-memory synchronization vs. message passing.

## Phase 2 — Threading

- [ ] **Thread lifecycle:** create, start, join, inspect, name, daemon/non-daemon and exception handling.
- [ ] **Thread state:** identifiers, thread-local data, \`Timer\`, \`Barrier\` and \`threading.excepthook\`.
- [ ] **Synchronization:** \`Lock\`, \`RLock\`, \`Event\`, \`Condition\`, \`Semaphore\` and barriers.
- [ ] **Communication:** \`queue.Queue\`, \`SimpleQueue\`, \`LifoQueue\`, \`PriorityQueue\`, bounded queues and task completion.
- [ ] **Patterns:** producer-consumer, worker pools, task handoff and shared-state protection.
- [ ] **Executors/futures:** \`ThreadPoolExecutor\`, \`submit\`, \`map\`, \`Future\`, \`wait\`, \`as_completed\`, callbacks and exception retrieval.
- [ ] **Failure modes:** executor deadlocks, starvation, blocked workers, cancellation limits and shutdown.

## Phase 3 — Multiprocessing

- [ ] **Process lifecycle:** create, start, join, exit codes, sentinels, close, terminate and kill.
- [ ] **Start methods:** \`spawn\`, \`fork\`, \`forkserver\`, platform defaults and \`get_context()\`.
- [ ] **Windows requirements:** main guard, import-safe worker functions, pickling and \`freeze_support()\`.
- [ ] **Serialization:** picklable arguments/results, importability, copying costs and large data transfer.
- [ ] **IPC:** \`Queue\`, \`Pipe\`, \`Connection\`, managers/proxies and choosing the right channel.
- [ ] **Shared data:** shared memory, shared ctypes and synchronization primitives.
- [ ] **Pools:** \`Pool\`, \`ProcessPoolExecutor\`, chunking, worker initializers and worker recycling.
- [ ] **Reliability:** worker crashes, timeouts, abrupt termination, resource cleanup and shared-memory leaks.

## Phase 4 — Subprocesses and script execution

- [ ] **Execution choices:** imports, \`runpy\`, \`python script.py\`, \`python -m\`, \`subprocess.run()\` and \`Popen()\`.
- [ ] **Interpreter selection:** \`sys.executable\`, other virtual environments, executable discovery and script paths.
- [ ] **Configuration:** arguments, \`cwd\`, environment variables, encoding and shell/quoting rules.
- [ ] **Lifecycle:** \`poll\`, \`wait\`, return codes, errors, timeouts, terminate and kill.
- [ ] **Streams:** stdin/stdout/stderr, pipes, \`communicate()\`, buffering, streaming output and pipe deadlocks.
- [ ] **OS details:** signals, process groups/trees, inherited handles and Windows-specific process behaviour.
- [ ] **Protocols:** line-based/JSON messages, readiness, health checks and continuous parent-child communication.

## Phase 5 — Asyncio

- [ ] **Fundamentals:** coroutine functions, coroutines, awaitables, \`Task\`, \`Future\` and event-loop scheduling.
- [ ] **Cooperative execution:** suspension points, yielding, blocking-call hazards and non-blocking libraries.
- [ ] **Task management:** \`create_task\`, \`gather\`, \`wait\`, \`as_completed\` and structured concurrency with \`TaskGroup\`.
- [ ] **Failure/cancellation:** exception propagation, \`ExceptionGroup\`, cancellation, shielding, timeouts and cleanup.
- [ ] **Coordination:** \`asyncio.Queue\`, locks, events, conditions and semaphores; understand that asyncio primitives are not thread-safe.
- [ ] **Async data handling:** streams, sockets, async iterators/generators and async context managers.
- [ ] **Networking:** TCP/UDP concepts, clients/servers, protocols, reconnects and timeouts.
- [ ] **Integration:** \`to_thread\`, \`run_in_executor\`, process pools, thread-safe loop handoff and async subprocesses.
- [ ] **Diagnostics:** asyncio debug mode, task inspection, unhandled exceptions and event-loop shutdown.

## Phase 6 — Concurrency patterns and reliability

- [ ] **Work distribution:** producer-consumer, worker pools, pipelines, fan-out/fan-in and map-reduce.
- [ ] **Flow control:** bounded queues, backpressure, rate limiting, batching and load shedding.
- [ ] **Scheduling:** priorities, fairness, recurring jobs, deadlines and starvation prevention.
- [ ] **Supervision:** worker monitoring, health checks, retries/backoff, restart policies and failure isolation.
- [ ] **Lifecycle:** cancellation propagation, cooperative stop signals, graceful shutdown and shutdown ordering.
- [ ] **Hybrid systems:** threads + asyncio, processes + asyncio, subprocesses + asyncio and cross-boundary messaging.

## Phase 7 — Testing, debugging and performance

- [ ] **Testing:** deterministic coordination, stress tests, race reproduction, timeouts and leak detection.
- [ ] **Debugging:** logging with process/thread/task identity, hung-worker diagnosis and exception reporting.
- [ ] **Measurement:** sequential baselines, repeatable benchmarks, profiling, latency and throughput.
- [ ] **Capacity:** worker counts, queue sizes, memory, file handles, CPU use and overload behaviour.
- [ ] **Resilience:** test crashes, partial failure, lost messages, slow workers and shutdown during active work.

## Phase 8 — Pygame integration

- [ ] Keep display, event pumping, rendering and game-state mutation on the main thread.
- [ ] Define safe worker inputs/results; do not pass live scenes/entities/window objects to workers.
- [ ] Add result, error and progress delivery to the game loop.
- [ ] Explore threaded file/asset I/O and safe handoff of decoded/converted assets.
- [ ] Explore process-based procedural generation and CPU-heavy calculations.
- [ ] Explore async networking and multiplayer communication.
- [ ] Handle stale results when scenes change; define global vs. scene-owned task lifetimes.
- [ ] Define cancellation, failure handling, shutdown order and resource cleanup.
- [ ] Preserve the synchronous game loop initially; consider an explicit async entry point later.
- [ ] Benchmark frame time, frame pacing, input responsiveness and task latency.

## Phase 9 — Advanced applications (after the fundamentals)

- [ ] **Script runner:** launch scripts/interpreters, select environments, pass configuration and collect results.
- [ ] **Process orchestration:** run multiple scripts, exchange data, monitor health, restart failures and shut down gracefully.
- [ ] **Mods/plugins:** compare in-process plugins with separate processes; design APIs, protocols, lifecycle and crash handling.
- [ ] **Mod security:** permissions and isolation; a subprocess alone is not a security sandbox.
- [ ] **External services:** dedicated servers, simulations and companion applications.
- [ ] **Development tools:** asset pipelines, FFmpeg recording/conversion, builds and background testing.

## Phase 10 — pygame_handler API and documentation

- [ ] Keep concurrency separate from scene/event internals; define ownership and lifecycle boundaries.
- [ ] Design task handles, status, results, exceptions, progress and cancellation.
- [ ] Keep thread, process and subprocess management distinct where their semantics differ.
- [ ] Add examples, tests, benchmarks and platform-specific documentation.
- [ ] Avoid premature abstractions; each feature must have a demonstrated use case.
