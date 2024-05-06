#!/usr/bin/env python3
'''
Asynchronous coroutine that takes in an integer argument
named wait_random that waits for a random delay between 0 and max_delay
seconds and eventually returns it
'''
import random
import asyncio

async def wait_random(max_delay: int = 10) -> float:
    '''Waits for a random number of seconds.
    '''
    wait_time = random.random() * max_delay
    await asyncio.sleep(wait_time)
    return wait_time
