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
    pass

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

# init once, then it will swarm it self towards the end
class Swarm:

    start_position : tuple[int, int]
    end_position : tuple[int, int]
    swarm_of_objects : list[SwarmObject]
    obstacles : list[Obstacle]
    move_direction : tuple[int, int]
    start_radius : int

    # desc : pass the surface, init n_swarm_objects, init the obstacles
    def __init__(self, surface, start_radius : int, separation_radius : int, n_swarm_objects : int, mode : str, start_position : tuple[int, int],
                  end_position : tuple[int, int]) -> None: # mode is for fixed or random obstacles
        
        self.surface = surface
        self.n_swarm_objects = n_swarm_objects
        self.mode = mode 
        self.start_position = start_position
        self.end_position = end_position
        self.start_radius = start_radius
        self.separation_radius = separation_radius
        self.swarm_of_objects = []

        # initiate all swarm objects
        for i in range (self.n_swarm_objects):
            obj = SwarmObject(start_position[0], start_position[1], 1, 1, (255, 255, 0), 2) # 1 x 1 pixel of character
            self.swarm_of_objects.append(obj)
    
        # initiate the surface by the obstacles (implement later)



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
    def alignment(self) -> pg.Vector2 : 

        # return the velocity
        avg_velocity_x = 0
        avg_velocity_y = 0

        for boid in self.swarm_of_objects :
            avg_velocity_x += boid.velocity.x
            avg_velocity_y += boid.velocity.y

        avg_velocity_x /= len(self.swarm_of_objects) # unfortunately pygame is not supported for drawing in floats
        avg_velocity_y /= len(self.swarm_of_objects) # unfortunately pygame is not supported for drawing in floats, so i have to do integer division
        
        alignment_effect = pg.Vector2(avg_velocity_x, avg_velocity_y)

        return alignment_effect

    # calculate the cohesion rule
    def cohesion(self) -> pg.Vector2 : 

        # return the velocity
        avg_position_x = 0
        avg_position_y = 0

        for boid in self.swarm_of_objects :
            avg_position_x += boid.pos.x
            avg_position_y += boid.pos.y

        avg_position_x /= len(self.swarm_of_objects)
        avg_position_y /= len(self.swarm_of_objects)
        
        cohesion_effect = pg.Vector2(avg_position_x, avg_position_y)

        return cohesion_effect      

    # calculate the final value change caused by the boids algorithm + auto update
    def boidsAlgorithm(self) -> None:

        # determine the cohesion and alignment effect
        cohesion_effect : pg.Vector2 = self.cohesion()
        alignment_effect : pg.Vector2 = self.alignment()

        for boid in self.swarm_of_objects:
            separation_effect = self.separation(boid)

            # calculate the final effect + update current boid
            boid.update(separation_effect, alignment_effect, cohesion_effect)

    # main function to move the swarm fro the start to the finish
    def run(self) -> None:
        # for each boids, do boids algorithm
        self.boidsAlgorithm()