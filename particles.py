
import pygame 
from settings import *
from sprites import BG 

FULL_RED = (255,0,0) 
FULL_GREEN = (0,255,0) 
FULL_BLUE = (0,0,255)  
FULL_YELLOW = (255,255,0) 
FULL_CYAN = (0,255,255)  
FULL_WHITE = (255,255,255)
FULL_PURPLE = (255,0,255) 
LIGHT_BLUE = (30 , 102 , 204) 
LIGHT_ORANGE = (204,102 , 30)  
LIGHT_GREEN = (102,204,30) 
LIGHT_PURPLE = (102,30,204)   
LIGHT_YELLOW = (255,255,51) 
LEMON_JUICE = (204,204,0) 


MAIN_ORANGE = (255,165,0)  
LIGHT_ORANGE = (255,153,51) 
GOLDEN_ORANGE = (204,102,0)

CLASSIC_NYAN_COLORS = [FULL_RED , MAIN_ORANGE , FULL_YELLOW , FULL_GREEN , LIGHT_BLUE , FULL_PURPLE ]  
GOLDEN_NYAN_COLORS = [FULL_WHITE , FULL_YELLOW , LIGHT_YELLOW , LEMON_JUICE ,LIGHT_ORANGE , GOLDEN_ORANGE  ]



CLASSIC_NYAN_PARTICLE_SPEED = pygame.math.Vector2(-100 , 0) 

class ClassicNyanParticle: 
    
    def __init__(self , player : pygame.sprite.Sprite , scale_factor : float ) -> None:
        self.particles = [] 
        self.display_surface = pygame.display.get_surface()
        self.player = player 
        self.size = 12 * scale_factor
        self.v_x = -1   

    def add_particle(self , color , offset_x = 0 , offset_y = 0): 
        pos_x , pos_y = self.player.rect.center  
        pos_x += offset_x 
        pos_y += offset_y 
        rect = pygame.Rect((pos_x , pos_y) , (self.size , self.size)) 
        self.particles.append((rect , color))

    def delete_particle(self): 
        particles_copy = [particle for particle in self.particles if particle[0].centerx > 0] 
        self.particles = particles_copy

    def emit(self): 
        self.delete_particle() 
        for particle in self.particles :  
            rect = particle[0] 
            rect.centerx += self.v_x
            pygame.draw.rect( self.display_surface , particle[1] , rect) 

                
                 



