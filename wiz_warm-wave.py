#!/usr/bin/env python3
import asyncio
from pywizlight import wizlight, PilotBuilder

async def travel_warm_white(bulbs, delay):
    """Travel warm white color down the string of bulbs."""
    while True:  # Infinite loop for continuous effect
        for i, bulb in enumerate(bulbs):
            # Turn the current bulb to warm white
            await bulb.turn_on(PilotBuilder(cool_white=255))
            await asyncio.sleep(delay)

            # Turn off the previous bulb, including wrapping around for the last bulb
            if i > 0:
                await bulbs[i-1].turn_off()
            elif i == len(bulbs) - 1:
                # Ensuring the first bulb is also turned off when the last bulb lights up
                await bulbs[0].turn_off()

async def main():
    # Initialize bulbs, starting with the one ending in 18 and then looping back to 10
    bulbs = [wizlight("192.168.0.18")] + [wizlight(f"192.168.0.{10+i}") for i in range(9)]

    # Set the delay in seconds (e.g., 0.1 seconds)
    delay = 0.5

    # Start the warm white travel effect
    await travel_warm_white(bulbs, delay)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
