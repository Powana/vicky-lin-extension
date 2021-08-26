import pygame
import config
import serial

pygame.init()
j = pygame.joystick.Joystick(config.TM_JOYSTICK_NO)
j.init()

try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                event.button == 1
                    serial.send()
                print("Button Pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print("Button Released")

except KeyboardInterrupt:
    print("Quitting")
    j.quit()
