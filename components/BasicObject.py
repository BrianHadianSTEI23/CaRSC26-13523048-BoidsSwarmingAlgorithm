import pygame as pg
import random as rd

class BasicObject :

    # attributes
    pos : pg.Vector2
    color : tuple[int, int, int] # of format tuple of (r, g, b)
    surface : pg.Surface

    def __init__(self, x, y, w, h, color):
        self.pos = pg.Vector2(x, y)     # floats
        self.rect = pg.Rect(x, y, w, h)
        self.color = color

    def draw(self, surface):
        self.rect.topleft = (int(self.pos.x), int(self.pos.y)) 
        pg.draw.rect(surface, self.color, self.rect)

class Obstacle(BasicObject): # for the obstacles, only to be drawn so it does not need to be complex 
    def __init__(self, x, y, w, h, color):
        self.pos = pg.Vector2(x, y)     # floats
        self.rect = pg.Rect(x, y, w, h)
        self.color = color

class SwarmObject(BasicObject):

    velocity : pg.Vector2 = pg.Vector2(0, 0)

    def __init__(self, x, y, w = 1, h = 1, color = (255, 255, 0), speed = 2):
        super().__init__(x, y, w, h, color)
        self.speed = speed
        self.velocity = pg.Vector2(
            rd.uniform(-1, 1),
            rd.uniform(-1, 1)
        )

    def update(self, separation_effect : pg.Vector2, alignment_effect : pg.Vector2, cohesion_effect : pg.Vector2) : # for updating
        self.velocity += separation_effect + alignment_effect + cohesion_effect

        if self.velocity.length() > self.speed:
            self.velocity.scale_to_length(self.speed)

        self.pos += self.velocity

# init once, then it will swarm it self towards the end
class Swarm:

    start_position : tuple[int, int]
    end_position : tuple[int, int]
    swarm_of_objects : list[SwarmObject]
    obstacles : list[Obstacle]
    move_direction : tuple[int, int]
    start_radius : int
    surface : pg.Surface

    # constructor : pass the surface, init n_swarm_objects, init the obstacles
    def __init__(self, surface : pg.Surface, start_radius : int, separation_radius : int, n_swarm_objects : int, mode : str, start_position : tuple[int, int],
                  end_position : tuple[int, int]) -> None: # mode is for fixed or random obstacles
        
        self.surface = surface
        self.n_swarm_objects = n_swarm_objects
        self.mode = mode 
        self.start_position = start_position
        self.end_position = end_position
        self.start_radius = start_radius
        self.separation_radius = separation_radius
        self.swarm_of_objects = []
        self.obstacles = []

        # initiate all swarm objects
        for i in range (self.n_swarm_objects):
            obj = SwarmObject(start_position[0], start_position[1], 10, 10, (255, 255, 255), 2) # 1 x 1 pixel of character
            self.swarm_of_objects.append(obj)
    
        # initiate the surface by the obstacles (implement)
        if mode == "RANDOM" :
            for i in range(self.surface.get_height()):
                for j in range(self.surface.get_width()):
                    random_val = rd.uniform(-1, 1)
                    if (random_val > 0.9) : # if more than 0, then the obstacle would be drawn
                        obs = Obstacle(j, i, rd.randint(0, 2), rd.randint(0, 2), (255, 255, 255))
                        self.obstacles.append(obs)
        else : # if not unknown, then do it fixed using a certain pattern
            for i in range(self.surface.get_height()):
                for j in range(self.surface.get_width()):
                    if ((i % 3 == 0) or (j % 5 == 0)) : # if more than 0, then the obstacle would be drawn
                        obs = Obstacle(j, i, rd.randint(0, 2), rd.randint(0, 2), (255, 255, 255))
                        self.obstacles.append(obs)

    # calculate the separation rule (this will return the value of separation which has x and y component, and value of separation is the speed)
    def separation(self, current_boid : SwarmObject) -> pg.Vector2 :

        separation_effect : pg.Vector2 = pg.Vector2(0, 0)
        
        for other_boid in self.swarm_of_objects:
            if other_boid != current_boid:

                dist = current_boid.pos.distance_to(other_boid.pos)

                if dist < self.separation_radius and dist > 0: # the separation radius is useful when every object is placed on the same pixel in the window
                    separation_effect += (current_boid.pos - other_boid.pos) / dist

        return separation_effect
                
    # calculate the alignment rule
    def alignment(self, boid : SwarmObject):
        avg_vel = pg.Vector2(0, 0)
        for other in self.swarm_of_objects:
            avg_vel += other.velocity
        avg_vel /= len(self.swarm_of_objects)
        return (avg_vel) * 0.05

    # calculate the cohesion rule
    def cohesion(self, boid : SwarmObject) -> pg.Vector2 : 

        center = pg.Vector2(0, 0)
        for other in self.swarm_of_objects:
            center += other.pos
        center /= len(self.swarm_of_objects)
        return (center) * 0.01
  
    # calculate the final value change caused by the boids algorithm + auto update
    def boidsAlgorithm(self) -> None:

        # determine the cohesion and alignment effect

        for boid in self.swarm_of_objects:
            alignment_effect : pg.Vector2 = self.alignment(boid)
            cohesion_effect : pg.Vector2 = self.cohesion(boid)
            separation_effect : pg.Vector2 = self.separation(boid)

            # calculate the final effect + update current boid
            boid.update(separation_effect, alignment_effect, cohesion_effect)

    # bounce the walls : function to bounce if the position of it is near the wall
    def bounceWall(self) :

        for boid in self.swarm_of_objects:
            horizontal_padding, vertical_padding = boid.rect.size
            if (boid.pos.x < 0):
                boid.pos.x = 0
                boid.velocity.x *= -1
            elif (boid.pos.x > (self.surface.get_width() - horizontal_padding)):
                boid.pos.x = (self.surface.get_width() - horizontal_padding)
                boid.velocity.x *= -1

            if (boid.pos.y > (self.surface.get_height() - vertical_padding)):  # 2 is the padding 
                boid.velocity.y *= -1
                boid.pos.y = (self.surface.get_height() - vertical_padding)
            elif  (boid.pos.y < 0) :
                boid.velocity.y *= -1
                boid.pos.y = 0
                

    # main function to move the swarm fro the start to the finish
    def run(self) -> None:
        # for each boids, do boids algorithm
        self.boidsAlgorithm()

        # then check for each boid, if they hit the wall
        self.bounceWall()