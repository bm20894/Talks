import arcade, random
from . import WIDTH, HEIGHT, dim

dim = dim // 2

# start coins OMIT
class FallingCoin(arcade.Sprite):
    def update(self):
        self.center_y -= 2
        if self.top < dim:
            self.bottom = HEIGHT - dim
            self.center_x = random.randrange(dim, WIDTH - dim)

class RisingCoin(arcade.Sprite):
    def update(self):
        self.center_y += 2
        if self.bottom > HEIGHT:
            self.top = 0
            self.center_x = random.randrange(dim, WIDTH - dim)

class BouncingCoin(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < dim or self.right > WIDTH - dim:
            self.change_x *= -1
        if self.bottom < dim or self.top > HEIGHT- dim:
            self.change_y *= -1
# end coins OMIT
