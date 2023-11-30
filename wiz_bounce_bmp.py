#!/usr/bin/env python3
import asyncio
from flask import Flask, request, render_template
from pywizlight import wizlight, PilotBuilder
import time

app = Flask(__name__)
taps = []
current_bpm = 120

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tap', methods=['POST'])
def tap():
    global taps, current_bpm
    taps.append(time.time())
    if len(taps) > 1:
        intervals = [taps[i] - taps[i-1] for i in range(1, len(taps))]
        avg_interval = sum(intervals) / len(intervals)
        current_bpm = 60 / avg_interval
    return '', 204

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
async def flask_runner():
    """ Run the Flask app """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, app.run, '127.0.0.1', 5000)
async def main():
    # Initialize bulbs, starting with the one ending in 18 and then looping back to 10
    bulbs = [wizlight("192.168.0.18")] + [wizlight(f"192.168.0.{10+i}") for i in range(8)]

    # Set the delay in seconds for the bouncing effect
    bpm = 128.9

    # Start the bouncing and color alternating effect
    await bounce_and_color(bulbs, bpm)

    # Start the Flask runner and the bouncing/color alternating effect
    await asyncio.gather(
        flask_runner(),
        bounce_and_color(bulbs)  # Your existing asyncio function
    )

if __name__ == '__main__':
    asyncio.run(main())