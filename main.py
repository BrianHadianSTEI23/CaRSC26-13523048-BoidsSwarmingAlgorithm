import pygame
import sys
from components.BasicObject import *

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Flocking Algorithm Implementation")

clock = pygame.time.Clock()

# init the swarm objects
sw = Swarm(screen, 1, 25, 10, "RANDOM", (0, 0), (800, 600))

# Init the engine
running = True
while running:
    clock.tick(60) # fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))  # bg color

    # run the sw but only change the values, not draw it onto screen
    sw.run()

    # draw every swarm_object
    for b in sw.swarm_of_objects :
        b.draw(screen)

    # draw every obstacles
    for ob in sw.obstacles :
        ob.draw(screen)

    # buat display ke screen (simpelnya buat clrscr, trs didraw ulang)
    pygame.display.flip()

pygame.quit()
sys.exit()
