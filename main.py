import pygame
import sys
from components.BasicObject import *

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Flocking Algorithm Implementation")

clock = pygame.time.Clock()

# init the swarm objects
sw = Swarm(screen, 10, 2, 20, "RANDOM", (0, 0), (800, 600))

# Init the engine
running = True
while running:
    clock.tick(60) # fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))  # bg color
    pygame.display.flip()

    # run the sw 
    sw.run()

pygame.quit()
sys.exit()
