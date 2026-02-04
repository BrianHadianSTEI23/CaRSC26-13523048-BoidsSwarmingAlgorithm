import pygame
import sys
import components

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Flocking Algorithm Implementation")

clock = pygame.time.Clock()

# Init the engine
running = True
while running:
    clock.tick(60) # fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))  # bg color
    pygame.display.flip()

    # init the swarm objects
    # sw = components.BasicObject.swarm

    # run the sw 
    # sw.run()

pygame.quit()
sys.exit()
