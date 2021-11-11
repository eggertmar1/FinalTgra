from math import *

import pygame
from pygame import color
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()
        self.view_matrix = ViewMatrix()
        self.projection_matrix = ProjectionMatrix()

        self.view_matrix.look(Point(0.0, 2.0, 3.0), Point(0.0, 0.0, 0.0), Vector(0.0, 1.0, 0.0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.fov = pi / 2
        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.5, 10)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()
        self.sphere = Sphere(24, 48)

        self.sun     = Material(Color(0.9, 0.7, 0.3), Color(0.6, 0.4, 0.1), 10, Color(1.0, 0.8, 0.1), Color(0.3, 0.2, 0.2))

        self.red     = Material(Color(1.0, 0.3, 0.3), Color(0.6, 0.3, 0.3), 10, Color(0.0, 0.0, 0.0), Color(0.3, 0.2, 0.2))
        self.green   = Material(Color(0.3, 1.0, 0.3), Color(0.3, 0.6, 0.3), 10, Color(0.0, 0.0, 0.0), Color(0.2, 0.3, 0.2))
        self.blue    = Material(Color(0.3, 0.3, 1.0), Color(0.3, 0.3, 0.6), 10, Color(0.0, 0.0, 0.1), Color(0.2, 0.2, 0.3))

        self.global_ambient = Color(0.3, 0.3, 0.3)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.LEFT_key_down = False
        self.RIGHT_key_down = False

        self.light_position = Point(0.0, 0.0, -5.0)
        self.light_position_factor = 0.0
        self.speed = 5.0

        self.light_sun      = Light(self.light_position, Color(0.9, 0.7, 0.3), Color(0.6, 0.4, 0.1), Color(0.3, 0.2, 0.2))
        self.light_white    = Light(self.light_position, Color(0.9, 0.9, 0.9), Color(0.3, 0.3, 0.3), Color(0.5, 0.5, 0.5))
        self.light_red      = Light(self.light_position, Color(0.9, 0.1, 0.1), Color(0.9, 0.3, 0.3), Color(0.4, 0.2, 0.2))
        self.light_green    = Light(self.light_position, Color(0.1, 0.9, 0.1), Color(0.3, 0.9, 0.3), Color(0.2, 0.4, 0.2))
        self.light_blue     = Light(self.light_position, Color(0.1, 0.1, 0.9), Color(0.3, 0.3, 0.9), Color(0.2, 0.2, 0.4))

        self.my_cube_position = Point(0.0, 0.0, 0.0)
        self.my_cube_position_factor = 0.0
        self.floor_cube_pos = Point(-1.0, -1.0, 0)

        self.angle = 0



## UPDATE ##

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        if(self.LEFT_key_down):
            self.view_matrix.yaw(pi * delta_time)
        if(self.RIGHT_key_down):
            self.view_matrix.yaw(-pi * delta_time)

        self.light_position_factor += delta_time * self.speed * pi / 10
        self.light_position.x = -cos(self.light_position_factor) * 5.0
        self.light_position.y = -1.0 + sin(self.light_position_factor) * 5.0

        self.my_cube_position_factor += delta_time * pi
        self.my_cube_position.x = cos(self.my_cube_position_factor)

        print(self.angle)
        if self.floor_cube_pos.x >= -3:
            self.floor_cube_pos += Vector(-1.0, 0.0, 0.0) * delta_time
        else:
            self.angle += pi / 2 * delta_time
        

    def move(self, pos, vector):
        pos += vector

## DISPLAY ##

    def display(self):
        glEnable(GL_DEPTH_TEST)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        
        self.shader.set_light(self.light_sun)
        self.shader.set_global_ambient(self.global_ambient)
        self.shader.set_eye_position(self.view_matrix.eye) # Added my code here

        self.model_matrix.load_identity()


    ## FIRST CUBE ##
        self.shader.set_material(self.red)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.my_cube_position.x, self.my_cube_position.y, self.my_cube_position.z)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()


    ## FLOOR - TWO PARTS ##
        self.shader.set_material(self.blue) # Adding Blue
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.floor_cube_pos.x, self.floor_cube_pos.y, self.floor_cube_pos.z)
        if self.floor_cube_pos.x <= -3:
            self.model_matrix.add_rotation_z(sin(self.angle))
        self.model_matrix.add_scale(1.8, 0.8, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.shader.set_material(self.green) # Adding green
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(1.0, -1.0, 0)
        self.model_matrix.add_scale(1.8, 0.8, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    ## SUN SPHERE
        self.shader.set_material(self.sun)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.light_position.x, self.light_position.y, self.light_position.z)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.shader.set_cut_off_position(-0.1)

        pygame.display.flip()



## PROGRAM EXECUTION ##

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True

                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_LEFT:
                        self.LEFT_key_down = False
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()