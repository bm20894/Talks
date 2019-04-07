import arcade
import random, math, sys, os
from utils import (FallingCoin, RisingCoin, BouncingCoin,
        WIDTH, HEIGHT, scale, dim, Worker, check_press, check_release,
        graph, coin_prob, Player, Button, STARTSCORE, COINSCORE)
from utils import questions

MOVESPEED = 5
TIMELIMIT = 30

# constants holding game states
GAMERUN = 1
GAMEOVER = 2
QUESTION = 3
GRAPH = 4

scl = scale / 4
d = scl * 200

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        super().__init__(width, height, title)
        self.game_state = 0
        self.coin_list = None

    def level(self):
        if self.game_state:
            self.game_state = GAMERUN
        self.coin_list = arcade.SpriteList()
        self.start_timer()

        levels = [ // HL
            (arcade.Sprite, 30), // HL
            (FallingCoin, 30), // HL
            (RisingCoin, 20), // HL
            (BouncingCoin, 20) // HL
        ] // HL
        try:
            self.coin_type, num_coins = levels[self.level_number] // HL
        except IndexError:
            self.game_state = GAMEOVER
            return
        else:
            self.make_walls()
            # end level OMIT

    def place_coin(self):
        while True:
            coin = self.coin_type('bin/gold/gold0.png', scale=0.3)
            coin.center_x = random.randrange(WIDTH)
            coin.center_y = random.randrange(HEIGHT)
            if isinstance(coin, BouncingCoin):
                coin.change_x = random.randrange(-3, 3)
                coin.change_y = random.randrange(-3, 3)
            # check for collisions
            wall_hits = arcade.check_for_collision_with_list(coin, self.wall_list)
            worker_hits = arcade.check_for_collision_with_list(coin, self.worker_list)
            cube_hits = arcade.check_for_collision_with_list(coin, self.cubicle_list)
            coin_hits = arcade.check_for_collision_with_list(coin, self.coin_list)

            if len(wall_hits) == len(coin_hits)\
                   == len(cube_hits) == len(worker_hits) == 0:
                break
        self.coin_list.append(coin)

    def make_walls(self):
        for w in self.wall_list:
            self.all_sprites.remove(w)
        self.wall_list = arcade.SpriteList()
        for x in range(0, WIDTH, dim):
            wall_t = arcade.Sprite('bin/wall.jpg', scale)
            wall_b = arcade.Sprite('bin/wall.jpg', scale)
            wall_t.center_x, wall_t.center_y = x, 0
            wall_b.center_x, wall_b.center_y = x, HEIGHT
            self.wall_list.append(wall_t)
            self.wall_list.append(wall_b)

        for y in range(0, HEIGHT, dim + 1):
            wall_l = arcade.Sprite('bin/wall.jpg', scale)
            wall_r = arcade.Sprite('bin/wall.jpg', scale)
            wall_l.center_x, wall_l.center_y = 0, y
            wall_r.center_x, wall_r.center_y = WIDTH, y
            self.wall_list.append(wall_l)
            self.wall_list.append(wall_r)

        self.make_cubicles()
        for wall in self.wall_list:
            self.all_sprites.append(wall)

    def cube_one(self):
        for y in range(int(d), int(1.5*dim)+1, int(d)):
            wall = arcade.Sprite('bin/wall.jpg', scl)
            wall.center_x, wall.center_y = 2.5*dim, y + dim/2 - d/2
            self.cubicle_list.append(wall)

        for y in range(int(HEIGHT-d), HEIGHT-int(1.5*dim)+1, int(-d)):
            wall = arcade.Sprite('bin/wall.jpg', scl)
            wall.center_x, wall.center_y = WIDTH - 2.5*dim, y - dim/2 + d/2
            self.cubicle_list.append(wall)

    def cube_two(self):
        comp = arcade.Sprite('bin/other/comp.png', 0.05)
        comp.center_x, comp.center_y = WIDTH - 165, 535
        comp.angle = 90
        self.wall_list.append(comp)

        comp = arcade.Sprite('bin/other/comp.png', 0.05)
        comp.center_x, comp.center_y = dim - 20, HEIGHT - 505
        comp.angle = 90
        self.wall_list.append(comp)

    def cube_three(self):
        comp = arcade.Sprite('bin/other/comp.png', 0.05)
        comp.center_x, comp.center_y = WIDTH - 60, HEIGHT - 505
        comp.angle = -90
        self.wall_list.append(comp)

        comp = arcade.Sprite('bin/other/comp.png', 0.05)
        comp.center_x, comp.center_y = 60, HEIGHT - 65
        comp.angle = 90
        self.wall_list.append(comp)

        comp = arcade.Sprite('bin/other/comp.png', 0.05)
        comp.center_x, comp.center_y = 240, HEIGHT - 65
        comp.angle = 90
        self.wall_list.append(comp)

        comp = arcade.Sprite('bin/other/comp.png', 0.05)
        comp.center_x, comp.center_y = 440, HEIGHT - 65
        comp.angle = 90
        self.wall_list.append(comp)

        for y in range(int(d), int(1.5*dim), int(d)):
            wall = arcade.Sprite('bin/wall.jpg', scl)
            wall.center_x, wall.center_y = 2.5*dim, HEIGHT - (y + dim/2 - d/2)
            self.cubicle_list.append(wall)

        for y in range(int(d), int(1.5*dim), int(d)):
            wall = arcade.Sprite('bin/wall.jpg', scl)
            wall.center_x, wall.center_y = WIDTH/2 , HEIGHT - (y + dim/2 - d/2)
            self.cubicle_list.append(wall)

        for y in range(int(HEIGHT-d), HEIGHT-int(1.5*dim)+1, int(-d)):
            wall = arcade.Sprite('bin/wall.jpg', scl)
            wall.center_x, wall.center_y = WIDTH - 2.5*dim, HEIGHT - (y - dim/2 + d/2)
            self.cubicle_list.append(wall)

    def cube_four(self):
        water = arcade.Sprite('bin/other/water.png', 0.2)
        water.center_x, water.center_y = WIDTH/2, dim + 12
        self.cubicle_list.append(water)

    def make_cubicles(self):
        self.cubicle_list = arcade.SpriteList()
        cube_levels = [self.cube_one, self.cube_two, self.cube_three, self.cube_four]
        for level in range(self.level_number+1):
            cube_levels[level]()
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.cubicle_list)

    def setup(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.all_sprites = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.cubicle_list = arcade.SpriteList()
        self.worker_list = arcade.SpriteList()
        self.button_list = []

        self.score = STARTSCORE
        self.coin_type = arcade.Sprite
        self.level_scores = []
        self.level_number = 0
        self.question_up = False
        self.question = None
        self.graphing = False
        self.touching = None

        player_images = [
            [arcade.load_texture('bin/boehm_walk/walk_boehm0.png', scale=0.75)],
            [arcade.load_texture('bin/boehm_walk/walk_boehm0.png', scale=0.75, mirrored=True)],
            [arcade.load_texture('bin/boehm_walk/walk_boehm{}.png'.format(i), scale=0.75) for i in range(6)],
            [arcade.load_texture('bin/boehm_walk/walk_boehm{}.png'.format(i), scale=0.75, mirrored=True) for i in range(6)]
        ]

        self.player = Player(player_images)

        # start a level
        self.level()
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.cubicle_list)

    def make_worker(self):
        worker = Worker()

        # use cubicle coordinates
        counter = 0
        while True:
            counter += 1
            worker.center_x, worker.center_y = worker.get_coords(self.level_number)
            plist = arcade.SpriteList()
            plist.append(self.player)
            player_hits = arcade.check_for_collision_with_list(worker, plist)
            worker_hits = arcade.check_for_collision_with_list(worker, self.worker_list)

            if len(worker_hits) == len(player_hits) == 0:
                break
            if counter == len(Worker.coords):
                return

        self.worker_list.append(worker)
        self.all_sprites.append(worker)

    def check_worker_collisions(self):
        p = self.player
        for worker in self.worker_list:
           if p.left > worker.right:
               continue
           if p.right < worker.left:
               continue
           if p.bottom > worker.top:
               continue
           if p.top < worker.bottom:
               continue
           self.touching = worker
           self.start_question()

    def start_question(self):
        self.game_state = QUESTION
        self.get_question()

    def start_timer(self):
        self.time = TIMELIMIT
        self.timing = True

    def stop_timer(self):
        self.timing = False

    def get_question(self):
        worker = self.touching
        buttons, data = worker.ask_question()
        for b in buttons:
            self.button_list.append(b)
        self.question = {
            'text': data.text,
            'buttons': data.buttons
        }
        # remove worker
        worker.kill()
        self.touching = None

    def draw_question(self):
        # draw dialog box with text
        x, y = 50, HEIGHT / 2
        w, h = WIDTH - 50 - x, HEIGHT - 50 - y
        x += w/2
        y += h/2
        arcade.draw_rectangle_filled(x, y, w, h, arcade.color.WHITE)
        arcade.draw_text(self.question['text'], x, y, arcade.color.BLACK, 14, width=w,
                align='center', anchor_x='center', anchor_y='center')
        # maybe stop time here
        self.stop_timer()
        self.draw_time()

        if not self.question_up:
            self.question_up = True
        for b in self.button_list:
            b.draw()

    def draw_title(self):
        tex = arcade.load_texture('bin/title.png')
        arcade.draw_texture_rectangle(WIDTH//2, HEIGHT//2, tex.width, tex.height, tex, 0)

    def draw_game_over(self):
        self.stop_timer()
        w = WIDTH/4
        arcade.draw_text('Game Over', w, 400, arcade.color.BLACK, 50, width=w*2, align='center')
        arcade.draw_text('Click to Restart', w, 350, arcade.color.BLACK, 24, width=w*2, align='center')

    def draw_game(self):
        if self.game_state == GAMERUN:
            r, g, b = arcade.color.AMAZON
            output = 'Quarter {}'.format(self.level_number + 1)
            arcade.draw_text(output, WIDTH/4, 25 + dim, (r-15, g-15, b-15), 50, width=WIDTH/2, align='center')

        self.player.draw()

        self.all_sprites.draw()
        self.cubicle_list.draw()
        self.coin_list.draw()

        output = 'Balance: ${}'.format(self.score)
        arcade.draw_text(output, 10, HEIGHT-20, arcade.color.WHITE, 18)
        output = 'Press [q] to quit'
        arcade.draw_text(output, WIDTH/2-50, HEIGHT-20, arcade.color.WHITE, 14)
        self.draw_time()

    def draw_time(self):
        output = 'Time: {:.0f}'.format(self.time)
        arcade.draw_text(output, WIDTH-115, HEIGHT-20, arcade.color.WHITE, 18)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        if not self.game_state:
            self.draw_title()
        if self.game_state == GAMERUN:
            self.draw_game()
        if self.game_state == GAMEOVER:
            self.draw_graph()
            self.draw_game_over()
        if self.game_state == QUESTION:
            self.draw_question()
        if self.game_state == GRAPH:
            self.draw_graph()

    def on_key_press(self, key, modifiers):
        SPEED = 5
        if key == arcade.key.Q:
            sys.exit(0)

        if key == arcade.key.UP:
            self.player.change_y = SPEED
        if key == arcade.key.DOWN:
            self.player.change_y = -SPEED
        if key == arcade.key.LEFT:
            self.player.change_x = -SPEED
        if key == arcade.key.RIGHT:
            self.player.change_x = SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button_num, modifiers):
        if not self.game_state:
            self.game_state = GAMERUN
        if check_press(x, y, self.button_list):
            self.game_state = QUESTION
        if self.game_state == GAMEOVER:
            self.game_state = GAMERUN
            self.setup()

    def on_mouse_release(self, x, y, button_num, modifiers):
        data = check_release(x, y, self.button_list)
        if data and self.game_state == QUESTION:
            # reward player for answer
            reward = self.question['buttons'][data.lbl]
            self.score += reward
            self.game_state = GAMERUN
            self.timing = True
            self.button_list = []

        if self.game_state == GRAPH:
            arcade.set_background_color(arcade.color.AMAZON)
            self.graphing = False
            self.next_level()

    def next_level(self):
        self.start_timer()
        self.level_number += 1
        self.level()

    def draw_graph(self):
        if not self.graphing and self.game_state != GAMEOVER:
            self.level_scores.append(self.score)
        self.graphing = True
        if graph(self.level_scores, self):
            self.game_state = GAMEOVER

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        if self.timing:
            self.time -= delta_time
        if self.time <= 0:
            # show quarter update and go to next level
            self.game_state = GRAPH
            self.draw_graph()
        if self.game_state == GAMERUN:
            # randomly spawn a coin
            if random.randrange(coin_prob) == 0:
                self.place_coin()
            self.coin_list.update()

            # make workers
            if random.randrange(coin_prob*2) == 0:
                self.make_worker()

            self.all_sprites.update()

            self.physics_engine.update()

            self.player.update_animation()

            hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
            for coin in hit_list:
                coin.kill()
                self.score += COINSCORE

            self.check_worker_collisions()

def main():
    game = MyGame(WIDTH, HEIGHT, 'FBLA')
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
