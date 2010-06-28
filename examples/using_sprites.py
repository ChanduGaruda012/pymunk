import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d
import math, random
X,Y = 0,1


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600

def main():
            
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    
    ### Physics stuff
    pymunk.init_pymunk()
    space = pymunk.Space()
    space.gravity = Vec2d(0.0, -900.0)
    
    ## logo
    logo_img = pygame.image.load("pymunk_logo_googlecode.png")
    logos = []
    
    
    ### Static line
    static_body = pymunk.Body(pymunk.inf, pymunk.inf)
    static_lines = [pymunk.Segment(static_body, (11.0, 280.0), (407.0, 246.0), 0.0)
                    ,pymunk.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
                    ]
    for l in static_lines:
        l.friction = 0.5
    space.add_static(static_lines)

    ticks_to_next_spawn = 10
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        
        ticks_to_next_spawn -= 1
        if ticks_to_next_spawn <= 0:
            ticks_to_next_spawn = 100
            x = random.randint(20,400)
            y = 500
            angle = random.random() * math.pi
            vs = [(-23,26), (23,26), (0,-26)]
            mass = 10
            moment = pymunk.moment_for_poly(mass, vs)
            body = pymunk.Body(mass, moment)
            shape = pymunk.Poly(body, vs)
            shape.friction = 0.5
            body.position = x, y
            body.angle = angle
            
            space.add(body, shape)
            logos.append(shape)
       
        ### Update physics
        dt = 1.0/60.0
        for x in range(1):
            space.step(dt)
            
        ### Draw stuff
        screen.fill(THECOLORS["white"])

        for logo_shape in logos:
            # image draw
            p = logo_shape.body.position
            p = Vec2d(p.x, flipy(p.y))
            
            # we need to rotate 180 degrees because of the y coordinate flip
            angle_degrees = math.degrees(logo_shape.body.angle) + 180 
            rotated_logo_img = pygame.transform.rotate(logo_img, angle_degrees)
            
            offset = Vec2d(rotated_logo_img.get_size()) / 2.
            p = p - offset
            
            screen.blit(rotated_logo_img, p)
            
            # debug draw
            ps = logo_shape.get_points()
            ps = [(p.x, flipy(p.y)) for p in ps]
            ps += [ps[0]]
            pygame.draw.lines(screen, THECOLORS["red"], False, ps, 1)
           

        for line in static_lines:
            body = line.body
            
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = pv1.x, flipy(pv1.y)
            p2 = pv2.x, flipy(pv2.y)
            pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2], 2)

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))
        
if __name__ == '__main__':
    main()