import board
import time
import neopixel
pixels = neopixel.NeoPixel(board.D18,6,brightness=1)
print("Turn lights on")
pixels.fill((255,255,255))
time.sleep(5)
print("Turn lights off")
pixels.fill((0,0,0))
time.sleep(5)