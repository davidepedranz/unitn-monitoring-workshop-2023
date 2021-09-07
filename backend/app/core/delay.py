import asyncio
import functools
import random


def random_delay(min_delay: float, max_delay: float):  # type: ignore
    """
    Decorator to add a random delay before executing the function.

    :param min_delay: Min delay in seconds.
    :param max_delay: Max delay in seconds.
    :return: Decorator.
    """
    assert min_delay >= 0
    assert min_delay <= max_delay

    def decorator(f):  # type: ignore
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):  # type: ignore
            wait = random.uniform(min_delay, max_delay)
            await asyncio.sleep(wait)
            return await f(*args, **kwargs)

        return wrapper

    return decorator


def rare_delay(delay: float, probability: float):  # type: ignore
    """
    Decorator to add a fixed random delay before executing the function
    with a given probability.

    :param delay: Delay in seconds.
    :param probability: Probability of delaying the function execution.
    :return: Decorator.
    """
    assert probability >= 0
    assert probability <= 1

    def decorator(f):  # type: ignore
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):  # type: ignore
            number = random.random()
            if probability >= number:
                await asyncio.sleep(delay)
            return await f(*args, **kwargs)

        return wrapper

    return decorator
