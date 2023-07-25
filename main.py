import pygame as pg 
import sys
import time
from bird import Bird
from pipe import Pipe

pg.init()

class Game :
    def __init__(self):
        self.width = 600
        self.height = 768
        self.win = pg.display.set_mode((self.width , self.height))
        self.clock = pg.time.Clock()
        self.scale_fac = 1.5                            #multiply dimentions by this
        self.set_up()
        self.monitoring= False
        self.score = 0
        self.game_lost = False
        self.move_speed = 250
        self.bird = Bird(self.scale_fac)
        self.pipes = []
        self.pipe_gen_counter = 91
        self.is_enter = False
        self.font = pg.font.Font("assets/font.ttf", 22)
        self.score_text =self.font.render("Score : 0 ", True, (20,0,2))
        self.score_rect = self.score_text.get_rect(center= (120,30))
        
        self.font2 = pg.font.Font("assets/font.ttf", 30)
        self.restart_text =self.font2.render("Restart", True, (20,0,2))
        self.restart_rect = self.restart_text.get_rect(center= (300,705))

        # self.font3 = pg.font.Font("assets/font.ttf", 15)
        # self.restart_text =self.font3.render("Press Enter To Start", True, (220,0,2))
        # self.restart_rect = self.restart_text.get_rect(center= (300,320))

        self.game_started = True

        self.dead_sound = pg.mixer.Sound("assets/sfx/dead.wav")
        self.flap_sound = pg.mixer.Sound("assets/sfx/flap.wav")
        self.score_sound = pg.mixer.Sound("assets/sfx/score.wav")

        self.playsound1 = True
        self.playsound2= True
        

        self.game_loop()

  

    def game_loop(self):
       
        last_time = time.time()
       
        while True :
            
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
                if event.type == pg.KEYDOWN and self.game_started:
                    if event.key == pg.K_RETURN:
                        self.is_enter = True
                        self.bird.update_on = True
                       

                
                    if event.key == pg.K_SPACE and self.is_enter :
                        self.bird.flap(dt)
                        self.flap_sound.play()

                if event.type == pg.MOUSEBUTTONUP:
                    if self.restart_rect.collidepoint(pg.mouse.get_pos()):                 #mouse_click
                        self.restart_game()

                # if self.is_enter == False and :
                #     self.dead_sound.play()

                                         
             
                

            if not self.game_lost:
                if self.is_enter:           #moving ground
                    self.ground_rect.x -= int(self.move_speed*dt)
                    self.ground2_rect.x -= int(self.move_speed*dt)

                    if self.ground_rect.right <0 :
                        self.ground_rect.x = self.ground2_rect.right

                    if self.ground2_rect.right <0 :
                        self.ground2_rect.x = self.ground_rect.right

                    if self.pipe_gen_counter >90:           #creating pipes
                        self.pipes.append(Pipe(self.move_speed, self.scale_fac))
                        self.pipe_gen_counter =0
                    self.pipe_gen_counter +=1

                    

                    for pipe in self.pipes:             #moving pipes
                        pipe.update(dt)

                    if len(self.pipes) != 0 :                               #deleting pipes   
                        if self.pipes[0].pipe_up_rect.right< 0:                 #any rect , top or bottom, both have same x
                            self.pipes.pop(0)

                self.bird.update(dt)

            self.collision()
            self.check_score()
            self.draw()                      
            pg.display.update()
            self.clock.tick(60)


    def restart_game(self):
        self.score = 0
        self.score_text =self.font.render("Score : 0 ", True, (20,0,2))
        self.is_enter= False
        self.game_started = True
        self.pipes.clear()                      #clear pipes
        self.pipe_gen_counter = 91
        self.bird.reset_pos()
        self.playsound1 = True
        self.playsound2= True
        

    def check_score(self):
        if len(self.pipes)>0:
            if (self.bird.rect.left > self.pipes[0].pipe_up_rect.left and 
                self.bird.rect.right< self.pipes[0].pipe_up_rect.right and not self.monitoring):

                self.monitoring = True 
                
            if self.bird.rect.left >self.pipes[0].pipe_up_rect.right and self.monitoring :
                self.monitoring = False
                self.score += 1
                self.score_text= self.font.render(f"Score : {self.score} ", True, (20,0,2))
                if int(self.score )%10== 0  and self.score>0:
                        self.score_sound.play()
                

    def collision(self):
        if len(self.pipes):                             #if there's a pipe in list

            if (self.bird.rect.colliderect(self.pipes[0].pipe_up_rect) or
                 self.bird.rect.colliderect(self.pipes[0].pipe_down_rect)) :
                
                self.is_enter = False 
                self.game_started = False                             #updating doesnt stop: gravity works on bird
                if self.playsound2:
                    self.dead_sound.play()
                    self.playsound2= False
                    


            if self.bird.rect.bottom >600:
               
                self.bird.update_on =False               #stops updating bird
                self.is_enter = False
                self.game_started = False                   #stops game
                # if  self.is_enter==False and  self.game_started==False:
                if self.playsound1 and self.playsound2 :
                    self.dead_sound.play()
                    self.playsound1= False            


            
            

    def draw(self):
        self.win.blit(self.bg ,(0,-290))
        for pipe in self.pipes:
            pipe.draw(self.win)
        self.win.blit(self.ground, self.ground_rect)
        self.win.blit(self.ground2, self.ground2_rect)
        self.win.blit(self.bird.img, self.bird.rect)
        self.win.blit(self.score_text , self.score_rect)      
        if not self.game_started :
            self.win.blit(self.restart_text , self.restart_rect)
        

    def set_up(self):
        self.bg= pg.transform.scale(pg.image.load("assets/bg.png").convert_alpha(),(600, 1066))    #resizing image
        self.ground =pg.transform.scale_by(pg.image.load("assets/ground.png").convert_alpha(), self.scale_fac)
        self.ground_rect = self.ground.get_rect(center = (300, 700))
        self.ground2 =pg.transform.scale_by(pg.image.load("assets/ground.png").convert_alpha(), self.scale_fac)
        self.ground2_rect = self.ground2.get_rect(center = (900, 700))
        

game = Game()