import pygame

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                print("Button Pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print("Button Released")

except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()