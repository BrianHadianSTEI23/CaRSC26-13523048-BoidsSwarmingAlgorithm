import pygame as pg

class BasicObject :

    # attributes
    x : int
    y : int
    w : int
    h : int
    color : tuple[int, int, int] # of format tuple of (r, g, b)

    def __init__(self, x, y, w, h, color):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)

class Obstacle(BasicObject): # for the obstacles, only to be drawn so it does not need to be complex 
    pass

class SwarmObject(BasicObject):

    speed : int

    def __init__(self, x, y, w, h, color, speed):
        super().__init__(x, y, w, h, color)
        self.speed = speed

    def update(self) : # for control
        keys = pg.key.get_pressed()
        if (keys[pg.K_LEFT]) :
            self.rect.x -= self.speed
        elif (keys[pg.K_UP]) :
            self.rect.y += self.speed
        elif (keys[pg.K_DOWN]) :
            self.rect.y -= self.speed
        elif (keys[pg.K_RIGHT]) :
            self.rect.x += self.speed


# init once, then it will swarm it self towards the end
class Swarm:

    start_position : tuple[int, int]
    end_position : tuple[int, int]
    swarm_of_objects : list[SwarmObject]

    # desc : pass the surface, init n_swarm_objects, init the obstacles
    def __init__(self, surface, n_swarm_objects : int, mode : str, start_position : tuple[int, int],
                  end_position : tuple[int, int]) -> None: # mode is for fixed or random obstacles
        
        self.surface = surface
        self.n_swarm_objects = n_swarm_objects
        self.mode = mode 
        self.start_position = start_position
        self.end_position = end_position

        # initiate all swarm objects
        for i in range (0, self.n_swarm_objects):
            obj = SwarmObject(start_position[0], start_position[1], 1, 1, (255, 255, 0), 2) # 1 x 1 pixel of character
            self.swarm_of_objects.append(obj)
    
    # calculate the separation rule
    def separation_rule() : 
        pass
    
    # calculate the separation rule
    def alignment_rule() : 
        pass
    
    # calculate the separation rule
    def cohesion_rule() : 
        pass

    # main function to move the swarm fro the start to the finish
    def run():
        pass