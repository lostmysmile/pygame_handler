
from __future__ import annotations

import asyncio
import random
from pathlib import Path

import pygame


WORKERS = 5
TARGET_FPS = 60
DECODE_BUDGET = 5
QUEUE_SIZE = 0 #WORKERS * 2 +2
IMAGE_PATH = Path(r"C:\Users\mrmmo\Desktop\python\pygame_handler\src\debug_sprite.png")


STOP_WORKER = sentinel("STOP_WORKER")


#game instance variables

paths = asyncio.Queue()
results = asyncio.Queue(maxsize=QUEUE_SIZE)

async def image_reader(
    path: Path,
)  -> bytes:
    # Local file reading is blocking, so delegate it.
    return await asyncio.to_thread(path.read_bytes)


async def image_loader(
    paths: asyncio.Queue,
    results: asyncio.Queue,
):
    """Async worker coordinating blocking file reads."""

    while True:
        path = await paths.get()

        try:
            if path is STOP_WORKER:
                return

            try:
                data = await image_reader(path)
                await results.put((path, data, None))

            except OSError as error:
                await results.put((path, None, error))

        finally:
            paths.task_done()

def create_workers_for_paths(image_paths):
    for path in image_paths:
        paths.put_nowait(path)

    # One sentinel per worker.
    for _ in range(WORKERS):
        paths.put_nowait(STOP_WORKER)
    
    # Queue jobs.
async def main():
    pygame.init()

    screen = pygame.display.set_mode((1200, 700))
    pygame.display.set_caption("Pygame + asyncio")

    surfaces = []


    image_paths = [IMAGE_PATH] * 100

    create_workers_for_paths(image_paths)

    workers = [
        asyncio.create_task(
            image_loader(paths, results)
        )
    for _ in range(WORKERS)
    ]

    running = True
    completed = 0
    failed = 0

    frame_duration = 1 / TARGET_FPS

    try:
        while running:
            frame_start = asyncio.get_running_loop().time()

            # 1. Pygame events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 2. Consume a limited number of results.
            for _ in range(DECODE_BUDGET):
                try:
                    path, raw_data, error = results.get_nowait()

                except asyncio.QueueEmpty:
                    break

                try:
                    if error is not None:
                        failed += 1
                        print(f"Read failed: {path}: {error}")
                        continue

                    image = pygame.image.load(
                        path.name,
                        # This example demonstrates file-like data
                    ) if False else None

                    import io

                    image = pygame.image.load(
                        io.BytesIO(raw_data)
                    ).convert_alpha()

                    pos = (
                        random.randint(
                            0, screen.get_width() - image.get_width()
                        ),
                        random.randint(
                            0, screen.get_height() - image.get_height()
                        ),
                    )

                    surfaces.append((image, pos))

                except pygame.error as error:
                    failed += 1
                    print(f"Decode failed: {error}")

                finally:
                    completed += 1
                    results.task_done()

            # 3. Render.
            screen.fill((30, 30, 30))

            for image, pos in surfaces:
                screen.blit(image, pos)

            pygame.display.flip()

            # 4. Yield to asyncio rather than blocking the OS thread.
            elapsed = (
                asyncio.get_running_loop().time() - frame_start
            )

            await asyncio.sleep(
                max(0, frame_duration - elapsed)
            )

            # if completed == len(image_paths):
            if all(map(lambda worker: worker.cancelled(),workers)):
                running = False

    finally:
        # Cancel any remaining worker tasks.
        for worker in workers:
            worker.cancel()

        await asyncio.gather(
            *workers,
            return_exceptions=True,
        )

        pygame.quit()

    print(
        f"Loaded: {len(surfaces)} | "
        f"Failed: {failed}"
    )


if __name__ == "__main__":
    asyncio.run(main())
