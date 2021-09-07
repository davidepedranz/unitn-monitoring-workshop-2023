#!/usr/bin/env python3

import asyncio
import os
import random
import sys
from typing import Callable, Awaitable

import httpx


def main() -> None:
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        pass


async def main_async() -> None:
    url = os.environ.get("BACKEND", "http://localhost:5000")

    tasks = {
        call_non_existing_endpoint: 2.0,
        simulate_correct_flow: 0.1,
        run_easter_egg: 0.5,
    }

    async with httpx.AsyncClient(base_url=url) as client:
        await asyncio.gather(
            *(
                run_periodically(f, interval=interval, client=client)
                for f, interval in tasks.items()
            )
        )


async def run_periodically(
    f: Callable[[httpx.AsyncClient], Awaitable[None]],
    *,
    interval: float,
    client: httpx.AsyncClient,
) -> None:
    while True:
        await asyncio.sleep(interval)

        try:
            await f(client)
        except httpx.HTTPError as exc:
            print(
                f"HTTP call '{exc.request.method} {exc.request.url}' failed: {exc}",
                file=sys.stderr,
            )


async def call_non_existing_endpoint(client: httpx.AsyncClient) -> None:
    await client.get("/robot")


async def simulate_correct_flow(client: httpx.AsyncClient) -> None:
    # create an item
    text = "I am robot 🤖"
    response = await client.post("/todos/", json={"text": text})

    if response.status_code not in (200, 201, 204):
        return

    id_ = response.json()["id"]

    # update the item
    text = "I am a robot 🤖 ... or maybe a ghost 👻"
    await client.patch(f"/todos/{id_}", json={"text": text})

    # activate and deactivate the item
    await client.post(f"/todos/{id_}/activate")
    await client.post(f"/todos/{id_}/deactivate")

    # get the single item and the list
    await client.get(f"/todos/{id_}")
    await client.get("/todos/")

    # delete the item
    await client.delete(f"/todos/{id_}")


async def run_easter_egg(client: httpx.AsyncClient) -> None:
    fruits = ("🍎", "🍊", "🍐", "🍇", "🍌")
    university = ("UniTN 🎓", "UniTN 🎓🎓", "UniTN 🎓🎓🎓")
    objects = university + tuple(fruit * (i + 1) for i in range(3) for fruit in fruits)

    # create a item
    text = f"🤖 likes {random.choice(objects)}"
    response = await client.post("/todos/", json={"text": text})

    if response.status_code not in (200, 201, 204):
        return

    id_ = response.json()["id"]

    # delete the item most of the time
    if random.random() < 0.80:
        await client.delete(f"/todos/{id_}")


def _log_http_error(exc: httpx.HTTPError) -> None:
    print(
        f"HTTP call '{exc.request.method} {exc.request.url}' failed: {exc}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
