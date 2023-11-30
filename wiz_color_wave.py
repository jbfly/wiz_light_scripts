#!/usr/bin/env python3
import asyncio
import colorsys
from pywizlight import wizlight, PilotBuilder

def hsl_to_rgb(h, s, l):
    """Convert HSL color space to RGB."""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)

def color_gradient(step, total_steps):
    """Generate a smooth transition of HSL colors and convert to RGB."""
    hue = (step / total_steps) % 1  # Hue value cycles from 0 to 1
    saturation = 1  # Full saturation for vivid colors
    lightness = 0.5  # Fixed lightness
    return hsl_to_rgb(hue, saturation, lightness)

async def wave_bulbs(bulbs, steps, delay):
    """Create a wave effect across the bulbs."""
    for step in range(steps):
        for i, bulb in enumerate(bulbs):
            color = color_gradient(step + i, steps)
            await bulb.turn_on(PilotBuilder(rgb=color))
            await asyncio.sleep(delay)

async def main():
    # Initialize bulbs, starting with the one ending in 18 and then looping back to 10
    bulbs = [wizlight("192.168.0.18")] + [wizlight(f"192.168.0.{10+i}") for i in range(8)]

    # Set the delay in seconds (e.g., 0.1 seconds)
    delay = 0.03
    steps = 18  # Number of steps in the color gradient

    # Start the wave effect
    while True:  # Loop to continuously run the wave effect
        await wave_bulbs(bulbs, steps, delay)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
