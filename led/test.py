import time
import board
import neopixel

pixels1 = neopixel.NeoPixel(board.D18, 55, brightness=1)

time.sleep(1)
pixels1.fill((0, 0, 0))

pixels1[0] = (0, 220, 0)
pixels1[9] = (0, 220, 0)

time.sleep(0.6)

pixels1[1] = (50, 220, 0)
pixels1[8] = (50, 220, 0)

time.sleep(0.6)

pixels1[2] = (100, 220, 0)
pixels1[7] = (100, 220, 0)

time.sleep(0.6)

pixels1[3] = (150, 220, 0)
pixels1[6] = (150, 220, 0)

time.sleep(0.6)

pixels1[4] = (220, 220, 0)
pixels1[5] = (220, 220, 0)

time.sleep(0.6)

for i in range(7):
    for j in range(10):
        pixels1[j] = (220, 0, 0)
    time.sleep(0.1)
    pixels1.fill((0, 0, 0))
    time.sleep(0.1)

