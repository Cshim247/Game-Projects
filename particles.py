import pygame as pg

class Particle(pg.sprite.Sprite):
    def __init__(self, 
                 groups: pg.sprite.Group, 
                 pos: list[int], 
                 color: str, 
                 direction: pg.math.Vector2, 
                 speed: int):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed

    def create_surf(self):
        self.image = pg.Surface((4, 4)).convert_alpha()
        self.image.set_colorkey("black")
        pg.draw.circle(surface=self.image, color=self.color, center=(2, 2), radius=2)
        self.rect = self.image.get_rect(center=self.pos)