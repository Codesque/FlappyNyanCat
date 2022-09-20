import math
import random
import pygame 
from settings import *  
from support import *

class BG(pygame.sprite.Sprite):  
    def __init__(self , screen : pygame.Surface , scale_factor : float ) -> None:
        super().__init__()  
        
        bg_image = pygame.image.load("img/background.png").convert()  
        reverse_bg_image = pygame.transform.flip(bg_image , True , False ) 
        
        
        full_width = bg_image.get_width() * scale_factor 
        full_height = bg_image.get_height() * scale_factor   
        self.fw , self.fh = full_width , full_height  

        bg_image = pygame.transform.scale(bg_image , (full_width , full_height)) 
        reverse_bg_image = pygame.transform.scale(reverse_bg_image , (full_width , full_height))

        self.image = pygame.Surface((3 * full_width , full_height)) 
        self.image.blit(bg_image , (0,0) )  
        self.image.blit(reverse_bg_image , (full_width - 10 , 0)  ) 
        self.image.blit(bg_image , (2 * full_width - 15 , 0))
        

        
        
        self.rect = self.image.get_rect(topleft = (0,0)) 
        self.pos = pygame.math.Vector2(self.rect.topleft)  

    def update(self , world_offset : pygame.Vector2 , delta_time : float):  
        self.pos += world_offset 
        if self.rect.centerx <=  -self.fw//2 -28:  
            
            self.pos.x = 0
        self.rect.x = round(self.pos.x)  

class NyanCat(pygame.sprite.Sprite): 

    def __init__(self  , groups : pygame.sprite.Group , scale_factor : float) -> None:
        super().__init__(groups)   
        self.scale_factor = scale_factor 
        self.status = "normal"  
        self.previous_state = "normal"
        self.allframes = []
        self.allframes.append(import_img_convert_alpha())   
        self.allframes.append(import_img_convert_alpha("img/richNyan")) 
        self.frames = self.allframes[0] 
        self.frame_counter = 0
        self.image = pygame.surface.Surface([100 , 100])
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH/15 , WINDOW_HEIGHT/2))  

        self.mask = pygame.mask.from_surface(self.image) 

        self.animation_speed = 10  

        self.gravity_cons = 800 
        self.pos = self.rect.topleft 
        self.direction = pygame.math.Vector2(0,0)  


        # For golden form : 
        self.time_holder = 0 
        self.time_length = 7000

    def get_golden_from(self): 
        self.time_holder = pygame.time.get_ticks()

    def goldenTimer(self): 
        
        if self.status == "golden":
            current_time = pygame.time.get_ticks() 
            if current_time - self.time_holder > self.time_length: 
                self.status = "normal" 


    def wave_func(self): 
        value = math.sin(pygame.time.get_ticks())  
        if value > 0 : 
            return 255
        else : return 0 

    def animate(self , delta_time : float ): 

        if self.status == "normal": 
            if self.previous_state != "normal": 
                self.frame_counter = 0  
            self.frames = self.allframes[0]  
            self.previous_state = self.status
        else : 
            if self.previous_state == "normal": 
                self.frame_counter = 0 
            self.frames = self.allframes[1]  
            self.previous_state = "golden"
            

        self.frame_counter += self.animation_speed * delta_time  
        if self.frame_counter >= len(self.frames): 
            self.frame_counter = 0 
        self.image = self.frames[int(self.frame_counter)]  
        self.image = pygame.transform.scale(self.image , pygame.math.Vector2(self.image.get_size()) * self.scale_factor  )  





    def apply_gravity(self , delta_time : float ):  
        self.direction.y  += self.gravity_cons * delta_time 
        self.pos += self.direction * delta_time  
        self.rect.y = round(self.pos.y) 


         
    def jump(self , delta_time): 
        self.direction.y = -400
        
    def rotate(self , delta_time : float ): 
        rotated_image = pygame.transform.rotozoom(self.image , -self.direction.y * 0.1 , 1)
        self.image = rotated_image 
        self.mask = pygame.mask.from_surface(self.image)
    
    def golden_duration_fades(self):
        if self.status == "golden": 
            current_time = pygame.time.get_ticks() 
            if current_time - self.time_holder > self.time_length - self.time_length//10 : 
                        alpha = self.wave_func() 
                        self.image.set_alpha(alpha) 
        else : 
            self.image.set_alpha(255)

    def update(self , world_shift_vector : pygame.Vector2 , delta_time : float  ):  
        self.apply_gravity(delta_time)
        self.animate(delta_time)  
        self.rotate(delta_time) 
        self.goldenTimer() 
        self.golden_duration_fades()


        
class ObstacleNyanCat(pygame.sprite.Sprite): 

    def __init__(self , groups : pygame.sprite.Group , scale_factor : float) -> None:
        super().__init__(groups)  
        self.orientation = random.choice(('up' , 'down')) 
        self.frames = import_img_convert_alpha("img/missingNyan")  
        self.frames = [pygame.transform.scale(frame , pygame.math.Vector2(frame.get_size()) * scale_factor) for frame in self.frames]
        self.frame_counter = 0    
        self.image = self.frames[self.frame_counter]   
        self.mask = pygame.mask.from_surface(self.image)
        self.create() 
        self.animation_speed = 10  
        


    def animate(self , delta_time : float ):  
        self.frame_counter += self.animation_speed * delta_time  
        if self.frame_counter >= len(self.frames): 
            self.frame_counter = 0 
        self.image = self.frames[int(self.frame_counter)]    

    def create(self):  
        x = WINDOW_WIDTH + random.randint(40 , 100)
        if self.orientation == "down": 
            #self.image = pygame.transform.flip(self.image , False , True )  
            y = 0 + random.randint(-50 , -10)  
            self.rect = self.image.get_rect(midtop = (x,y))

        else : 
            y = WINDOW_HEIGHT + random.randint(10 , 50) 
            self.rect = self.image.get_rect(midbottom = (x , y))  

        self.pos = pygame.math.Vector2(self.rect.topleft)


    def update(self , world_shift : pygame.Vector2 , delta_time : float ): 
        
        self.pos.x -= 400 * delta_time 
        self.rect.x = round(self.pos.x) 

        
        self.animate(delta_time)   
        if self.orientation == "down":  
            self.image = pygame.transform.flip(self.image , True , True ) 

        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right <= -100 : 
            self.kill()
        
        

class FatDonutCat(pygame.sprite.Sprite): 

    def __init__(self , groups : pygame.sprite.Group , scale_factor : float ) -> None:
        super().__init__(groups)  
        self.frames = import_img_convert_alpha("img/fatNyan")  
        self.frames = [pygame.transform.scale(frame , pygame.math.Vector2(frame.get_size()) * scale_factor) for frame in self.frames]
        self.frame_counter = 0  
        self.animation_speed = 10
        self.image = self.frames[self.frame_counter]   
        self.creation()  
        self.mask = pygame.mask.from_surface(self.image)



    def creation(self): 
        border = 200 
        pos_y = random.randint(border , WINDOW_HEIGHT - border)    
        pos_x = WINDOW_WIDTH + random.randint(20 , 60) 
        self.rect = self.image.get_rect(topleft = (pos_x , pos_y) ) 


    def animate(self , delta_time : float ):  
        self.frame_counter += self.animation_speed * delta_time  
        if self.frame_counter >= len(self.frames): 
            self.frame_counter = 0 
        self.image = self.frames[int(self.frame_counter)] 
        self.mask = pygame.mask.from_surface(self.image)     

    def update(self , world_shift : pygame.math.Vector2 , delta_time : float): 
        pos_x = self.rect.centerx
        pos_x += -400 * delta_time 
        self.rect.centerx = round(pos_x)  
        self.animate(delta_time) 

        if self.rect.right <= -100 : 
            self.kill()  


class DogeCoin(pygame.sprite.Sprite):  

    def __init__(self, groups : pygame.sprite.Group , scale_factor : float) -> None:
        super().__init__(groups)  
        self.frames = import_img_convert_alpha("img/nyanDoggo_dogecoin")  
        self.frames = [pygame.transform.scale(frame , pygame.math.Vector2(frame.get_size()) * scale_factor) for frame in self.frames]
        self.frame_counter = 0  
        self.animation_speed = 10
        self.image = self.frames[self.frame_counter]   
        self.creation()  
        self.mask = pygame.mask.from_surface(self.image) 

    def creation(self): 
        border = 100
        pos_y = random.randint(border , WINDOW_HEIGHT - border)    
        pos_x = WINDOW_WIDTH + random.randint(20 , 60) 
        self.rect = self.image.get_rect(topleft = (pos_x , pos_y) )  

    def animate(self , delta_time : float ):  
        self.frame_counter += self.animation_speed * delta_time  
        if self.frame_counter >= len(self.frames): 
            self.frame_counter = 0 
        self.image = self.frames[int(self.frame_counter)] 
        self.mask = pygame.mask.from_surface(self.image)  


    def update(self , world_shift : pygame.math.Vector2 , delta_time : float): 
        pos_x = self.rect.centerx
        pos_x += -400 * delta_time 
        self.rect.centerx = round(pos_x)  
        self.animate(delta_time)  
        

        if self.rect.right <= -100 : 
            self.kill()  



        















    