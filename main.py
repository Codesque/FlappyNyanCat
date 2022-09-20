import pygame 
import sys , time

from settings import * 
from sprites import * 
from particles import *


        

class Game : 

    def __init__(self) -> None: 
        pygame.init() 
        self.screen = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT ))  
        self.clock = pygame.time.Clock()   
        self.all_sprites = pygame.sprite.Group() 
        self.barrier_sprites = pygame.sprite.Group()
           

        bg_height = pygame.image.load("img/background.png").get_height()  
        self.scale_factor = WINDOW_HEIGHT / bg_height   
        self.background_surface = BG(self.screen , self.scale_factor)
        self.all_sprites.add(self.background_surface) 
        self.offset_force = 600 
        self.world_shift_vector = 0  
        self.player_group = pygame.sprite.GroupSingle()
        self.player = NyanCat(self.player_group , self.scale_factor/15)   

        # Collect Doge Coins 
        self.coin_sprites = pygame.sprite.Group() 
        
        # GAME EVENTS 

        #obstacle_call
        self.obstacle_timer = pygame.USEREVENT + 1 
        pygame.time.set_timer(self.obstacle_timer , 1400) 

        # Classic Nyan Cat Particle Effects 
        self.classicNyanParticleEvent = pygame.USEREVENT + 2 
        pygame.time.set_timer(self.classicNyanParticleEvent , 20)  
        self.nyanEffect = ClassicNyanParticle(self.player , self.scale_factor * 0.25) 
        self.go_up = True  
        self.go_up_counter = 0 

        # Fat Donut Cat Caller 
        self.fatDonutCallEvent = pygame.USEREVENT + 3 
        pygame.time.set_timer(self.fatDonutCallEvent , 5000)  

        # Doge Coin Caller  
        self.callCyriptoEvent = pygame.USEREVENT + 4 
        pygame.time.set_timer(self.callCyriptoEvent , 12000 ) 
        self.TOTAL_COLLECTED_DOGE_COINS = 0


    def barrierCollide(self): 

        if pygame.sprite.spritecollide(self.player , self.barrier_sprites , False , pygame.sprite.collide_mask): 
            raise SystemExit 

    def coinCollide(self): 
        if pygame.sprite.spritecollide(self.player , self.coin_sprites , True , pygame.sprite.collide_mask):  
            self.TOTAL_COLLECTED_DOGE_COINS += 1  
            self.player.status = "golden" 
            self.player.get_golden_from() 
            print(self.TOTAL_COLLECTED_DOGE_COINS) 



        
    def run(self):
        last_time = time.time() 
        
        while True :  

            delta_time = time.time() - last_time 
            last_time = time.time()  
            self.world_shift_vector = pygame.math.Vector2((self.offset_force * delta_time) * -1 , 0) 
            
            

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    
                    pygame.quit() 
                    raise SystemExit  

                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_q: 
                        pygame.event.post(pygame.event.Event(pygame.QUIT))  

                    if event.key == pygame.K_w : 
                        self.player.jump(delta_time) 

                if event.type == self.obstacle_timer : 
                    ObstacleNyanCat([self.all_sprites , self.barrier_sprites] , self.scale_factor * 0.22) 

                if event.type == self.classicNyanParticleEvent :  

                    if self.player.status == "normal":
                        if self.go_up : 
                            for index , color in enumerate(CLASSIC_NYAN_COLORS): 
                                self.nyanEffect.add_particle(color , offset_y= (-26 + (12 * index)))  
                            self.go_up_counter += 1 
                            if self.go_up_counter >= 12 : 
                                self.go_up = False 
                                self.go_up_counter = 0  
                                
                        else :  
                            for index , color in enumerate(CLASSIC_NYAN_COLORS): 
                                self.nyanEffect.add_particle(color , offset_y= (-12 + (12 * index))) 
                            
                            self.go_up_counter += 1 
                            if self.go_up_counter >= 12 : 
                                self.go_up = True  
                                self.go_up_counter = 0   

                    elif self.player.status == "golden":
                        if self.go_up : 
                            for index , color in enumerate(GOLDEN_NYAN_COLORS): 
                                self.nyanEffect.add_particle(color , offset_y= (-26 + (12 * index)))  
                            self.go_up_counter += 1 
                            if self.go_up_counter >= 12 : 
                                self.go_up = False 
                                self.go_up_counter = 0  
                                
                        else :  
                            for index , color in enumerate(GOLDEN_NYAN_COLORS): 
                                self.nyanEffect.add_particle(color , offset_y= (-12 + (12 * index))) 
                            
                            self.go_up_counter += 1 
                            if self.go_up_counter >= 12 : 
                                self.go_up = True  
                                self.go_up_counter = 0  

                if event.type == self.fatDonutCallEvent : 
                    FatDonutCat([self.all_sprites , self.barrier_sprites] , self.scale_factor * 0.2)  

                if event.type == self.callCyriptoEvent: 
                    DogeCoin([self.all_sprites , self.coin_sprites] , self.scale_factor * 0.2) 




            self.screen.fill((0,0,0)) 
            
            self.all_sprites.update(self.world_shift_vector,delta_time) 
            self.all_sprites.draw(self.screen)  
            self.nyanEffect.emit() 
            self.player_group.update(self.world_shift_vector , delta_time) 
            self.player_group.draw(self.screen) 

            self.barrierCollide()  
            self.coinCollide()
             
            pygame.display.update()  



if __name__ == "__main__": 
    game = Game() 
    game.run()


