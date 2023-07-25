import pygame as pg

pg.init()

class Bird(pg.sprite.Sprite):
    def __init__(self, scale_fac):
        super(Bird, self).__init__()

        self.bird_img = [pg.transform.scale_by(pg.image.load("assets/birdup.png").convert_alpha(), scale_fac) ,
                     pg.transform.scale_by(pg.image.load ("assets/birddown.png").convert_alpha() , scale_fac)]
        self.img_switch = 0
        self.img = self.bird_img[self.img_switch]
        # self.reset_bird()
        self.rect = self.img.get_rect(center= (100,100))
        self.bird_speed = 250
        self.vel_y = 0
        self.gravity = 10
        self.update_on = False
        self.anim_counter = 0
        

    def update(self,dt):

        if self.update_on :
            # keys = pg.key.get_pressed()
            # if keys[pg.K_DOWN]:
            #     self.rect.y += self.bird_speed*dt
            # if keys[pg.K_UP]:
            #     self.rect.y -= self.bird_speed*dt 
           
            self.animation()
            self.grav(dt)

            if self.rect.y <= 0 and self.bird_speed == 250:
                self.rect.y = 0
                self.bird_speed = 0
                self.vel_y = 0
            elif self.rect.y >0:
                self.bird_speed = 250

        

    # def reset_bird (self):
        
    #     self.rect= pg.Rect(100 ,100, 34 , 24 )
    #     self.anim_counter =0
    #     self.img_switch = 1
        
    def flap(self, dt):
        self.vel_y =- self.bird_speed*dt 

    def grav(self, dt):
        self.vel_y += self.gravity*dt
        self.rect.y += self.vel_y


    def animation(self):
        if self.anim_counter == 8 :
            self.img = self.bird_img[self.img_switch]
            if self.img_switch == 1 : self.img_switch = 0
            else: self.img_switch =1
            self.anim_counter = 0
        self.anim_counter += 1

    def reset_pos(self):
        self.rect.center= (100,100)         #reset position
        self.vel_y = 0
        self.gravity = 10
        self.update_on = False
        self.anim_counter = 0