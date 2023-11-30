#!/usr/bin/env python3
import asyncio
from pywizlight import wizlight, PilotBuilder

def alternate_color(i):
    """Returns red or blue color based on the bulb index."""
    return (255, 0, 0) if i % 2 == 0 else (0, 0, 255)  # Red for even, blue for odd

async def bounce_and_color(bulbs, bpm):
    """Bouncing effect for one bulb while others alternate colors."""
    length = len(bulbs)
    delay = 60 / bpm  # Calculate delay from BPM
    while True:
        # Forward direction
        for i in range(length):
            for j, bulb in enumerate(bulbs):
                if j == i:
                    # Bouncing bulb - warm white
                    await bulb.turn_on(PilotBuilder(warm_white=255))
                else:
                    # Other bulbs - red/blue pattern
                    await bulb.turn_on(PilotBuilder(rgb=alternate_color(j)))
            await asyncio.sleep(delay)  # Use the calculated delay
            if i < length - 1:  # Turn off the bouncing bulb if it's not the last bulb
                await bulbs[i].turn_off()

        # Backward direction - starts and ends one bulb away from the ends
        for i in range(length - 2, 0, -1):
            for j, bulb in enumerate(bulbs):
                if j == i:
                    # Bouncing bulb - warm white
                    await bulb.turn_on(PilotBuilder(warm_white=255))
                else:
                    # Other bulbs - red/blue pattern
                    await bulb.turn_on(PilotBuilder(rgb=alternate_color(j)))
            await asyncio.sleep(delay)  # Use the calculated delay
            await bulbs[i].turn_off()  # Turn off the bouncing bulb

async def main():
    # Initialize bulbs, starting with the one ending in 18 and then looping back to 10
    bulbs = [wizlight("192.168.0.18")] + [wizlight(f"192.168.0.{10+i}") for i in range(8)]

    # Set the delay in seconds for the bouncing effect
    bpm = 128.9

    # Start the bouncing and color alternating effect
    await bounce_and_color(bulbs, bpm)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
