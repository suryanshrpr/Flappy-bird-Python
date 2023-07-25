import pygame as pg
from random import randint 

pg.init()

class Pipe(pg.sprite.Sprite) :
    def __init__(self, move_speed, scale_fac):
        super(Pipe , self).__init__()

        self.pipe_up = pg.transform.scale_by(pg.image.load("assets/pipeup.png").convert_alpha(), scale_fac)
        self.pipe_down = pg.transform.scale_by(pg.image.load("assets/pipedown.png").convert_alpha(), scale_fac)
        
        self.pipe_up_rect = self.pipe_up.get_rect()
        self.pipe_down_rect = self.pipe_down.get_rect()

        self.move_speed = move_speed
        self.pipe_dist = 200
        self.pipe_up_rect.y = randint(230, 530)
        self.pipe_up_rect.x = 600
        self.pipe_down_rect.y = self.pipe_up_rect.y- self.pipe_dist - self.pipe_up_rect.height
        self.pipe_down_rect.x= 600
        # self.img = self.pipes[random.randint(0,1)]
        # self.pipe_speed = move_speed

        # if self.img == self.pipes[1]:
        #     self.rect = pg.Rect(300, 320 ,52, 320)
        # if self.img == self.pipes[0]:
        #     self.rect = pg.Rect(300,380, 52 , 320)

    def draw(self,win):
        win.blit(self.pipe_up, self.pipe_up_rect)
        win.blit(self.pipe_down , self.pipe_down_rect)

    def update(self,dt):
        self.pipe_up_rect.x -= int(self.move_speed*dt)
        self.pipe_down_rect.x -= int(self.move_speed*dt)

    #     if self.pipe_up_rect.right <0 :
    #         self.delete_pipe()
    #     if self.pipe_down_rect.right <0:
    #         self.delete_pipe()

    # def delete_pipe(self):
    #     self.kill()
    #     del self

    