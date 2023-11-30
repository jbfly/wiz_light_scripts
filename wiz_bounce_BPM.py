import asyncio
from pywizlight import wizlight, PilotBuilder

def alternate_color(i):
    """Returns red or blue color based on the bulb index."""
    return (255, 0, 0) if i % 2 == 0 else (0, 0, 255)  # Red for even, blue for odd

async def bounce_and_color(bulbs):
    """Bouncing effect for one bulb while others alternate colors."""
    global current_bpm
    length = len(bulbs)
    while True:
        # Forward direction
        for i in range(length):
            # Update BPM at each step
            try:
                with open('bpm.txt', 'r') as f:
                    current_bpm = float(f.read()) + 23.95  # Correction factor
            except (FileNotFoundError, ValueError):
                current_bpm = 120  # Default BPM if file not found or invalid

            delay = 60 / current_bpm  # Calculate delay from BPM

            # Update bulbs
            for j, bulb in enumerate(bulbs):
                if j == i:
                    await bulb.turn_on(PilotBuilder(warm_white=255))
                else:
                    await bulb.turn_on(PilotBuilder(rgb=alternate_color(j)))
            await asyncio.sleep(delay)
            await bulbs[i].turn_off()

        # Backward direction
        for i in range(length - 2, 0, -1):
            # Update BPM at each step
            try:
                with open('bpm.txt', 'r') as f:
                    current_bpm = float(f.read()) + 23.95
            except (FileNotFoundError, ValueError):
                current_bpm = 120

            delay = 60 / current_bpm

            # Update bulbs
            for j, bulb in enumerate(bulbs):
                if j == i:
                    await bulb.turn_on(PilotBuilder(warm_white=255))
                else:
                    await bulb.turn_on(PilotBuilder(rgb=alternate_color(j)))
            await asyncio.sleep(delay)
            await bulbs[i].turn_off()


async def main():
    # Initialize bulbs, starting with the one ending in 18 and then looping back to 10
    bulbs = [wizlight("192.168.0.18")] + [wizlight(f"192.168.0.{10+i}") for i in range(8)]

    # Start the bouncing and color alternating effect
    await bounce_and_color(bulbs)

if __name__ == '__main__':
    asyncio.run(main())
