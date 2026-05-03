import numpy as np
import random
from config import *
import pygame

pygame.init()

BlockSize = 25
config = Config()

# dic stores all the arrays for each type of block, with the rotated ones too
blocks = {
    2: [np.array([[0, 1, 0], [1, 1, 0], [0, 1, 0]]), np.array([[0, 0, 0], [1, 1, 1], [0, 1, 0]]),
        np.array([[0, 1, 0], [0, 1, 1], [0, 1, 0]]), np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]])],
    3: [np.array([[1, 0, 0], [1, 1, 0], [0, 1, 0]]), np.array([[0, 0, 0], [0, 1, 1], [1, 1, 0]]),
        np.array([[0, 1, 0], [0, 1, 1], [0, 0, 1]]), np.array([[0, 1, 1], [1, 1, 0]])],
    4: [np.array([[0, 1, 0], [0, 1, 0], [1, 1, 0]]), np.array([[0, 0, 0], [1, 1, 1], [0, 0, 1]]),
        np.array([[0, 1, 1], [0, 1, 0], [0, 1, 0]]), np.array([[1, 0, 0], [1, 1, 1]])],
    5: [np.array([[1, 1, 0], [0, 1, 0], [0, 1, 0]]), np.array([[0, 0, 0], [1, 1, 1], [1, 0, 0]]),
        np.array([[0, 1, 0], [0, 1, 0], [0, 1, 1]]), np.array([[0, 0, 1], [1, 1, 1]])],
    6: [np.array([[0, 1], [0, 1], [0, 1], [0, 1]]), np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1]]),
        np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]), np.array([[0, 0, 0, 0], [1, 1, 1, 1]])],
    7: [np.array([[1, 1], [1, 1]]), np.array([[1, 1], [1, 1]]), np.array([[1, 1], [1, 1]]),
        np.array([[1, 1], [1, 1]])],
    8: [np.array([[0, 1, 0], [1, 1, 0], [1, 0, 0]]), np.array([[0, 0, 0], [1, 1, 0], [0, 1, 1]]),
        np.array([[0, 0, 1], [0, 1, 1], [0, 1, 0]]), np.array([[1, 1, 0], [0, 1, 1]])]
}

blocks_image = {
    2: pygame.transform.scale(pygame.image.load("assets/blocks/blue_block.png"), (BlockSize, BlockSize)),
    3: pygame.transform.scale(pygame.image.load("assets/blocks/cyan_block.png"), (BlockSize, BlockSize)),
    4: pygame.transform.scale(pygame.image.load("assets/blocks/green_block.png"), (BlockSize, BlockSize)),
    5: pygame.transform.scale(pygame.image.load("assets/blocks/pink_block.png"), (BlockSize, BlockSize)),
    6: pygame.transform.scale(pygame.image.load("assets/blocks/purple_block.png"), (BlockSize, BlockSize)),
    7: pygame.transform.scale(pygame.image.load("assets/blocks/red_block.png"), (BlockSize, BlockSize)),
    8: pygame.transform.scale(pygame.image.load("assets/blocks/yellow_block.png"), (BlockSize, BlockSize)),
}


class MovableBlocks:

    def __init__(self, game, color=None):
        if color is None:
            self.color_value = random.choice(list(blocks.keys()))
        else:
            self.color_value = color

        self.speed = 1
        self.state = 0
        self.array = blocks[self.color_value][self.state]
        self.game = game
        # we get the coordinates of each block of the movable_blocks
        self.co = self.get_co(self.game.a, True)
        # stores the actual positon of the array, so when it turns, it doesn't move right
        self.pos = [0, self.game.playing_screen_size[0] // 2 // BlockSize]

    def get_co(self, array: np.array, reverse: bool) -> list:
        """""
        returns the coordinates of every ones in a
        """""
        coords = np.argwhere(array == 1)
        # we sort the list with the biggest co in the first place so when we make
        # the blocks go down 1 block they don't destroy each other
        # you must reverse it or not depending on where the block will move, to understand this better make a scheme
        return sorted(map(list, coords), reverse=reverse)

    def simulate_right_turn(self) -> np.array:
        """""
        returns a turned array
        """""
        self.state += 1
        if self.state >= 4:
            self.state = 0
        return blocks[self.color_value][self.state]

    def simulate_left_turn(self) -> np.array:
        """""
        returns a turned array
        """""
        self.state -= 1
        if self.state <= -1:
            self.state = 3
        return blocks[self.color_value][self.state]

    def move(self, dx: int, dy: int):
        self.pos[0] += dy
        self.pos[1] += dx
        for coords in self.co:
            # hiding the old block
            self.game.a[coords[0], coords[1]] = 0
            self.game.a[coords[0] + dy, coords[1] + dx] = 1

    def can_move(self, dx: int, dy: int) -> bool:
        """""
        checks if the blocks can move in a direction
        """""
        movable = True
        for coords in self.co:
            if self.game.a[coords[0] + dy, coords[1] + dx] in range(config.data["first_fixed_block"],
                                                                    config.data["last_fixed_block"] + 1) or not (
                    0 <= coords[0] + dy < self.game.a.shape[0]) or not (0 <= coords[1] + dx < self.game.a.shape[1]):
                movable = False
                break
        return movable

    def can_fit(self, arr: np.array) -> bool:
        """""
        checks if the array can fit at the moving blocks position
        """""
        fit = True
        arr_co = self.get_co(arr, False)
        for coords in arr_co:

            if (self.game.a[coords[0] + self.pos[0], coords[1] + self.pos[1]]
                    in range(config.data["first_fixed_block"], config.data["last_fixed_block"] + 1)
                    or not (0 <= coords[0] + self.pos[0] < self.game.a.shape[0]) or not (
                            0 <= coords[1] + self.pos[1] < self.game.a.shape[1])):
                fit = False
                break
        return fit


class Game:

    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen

        self.playing_screen_size = (config.data["playing_screen_width"], config.data["playing_screen_height"])
        # creating the numpy array
        self.arr_size = (self.playing_screen_size[1] // BlockSize, self.playing_screen_size[0] // BlockSize)
        self.a = np.zeros(self.arr_size)

        self.movable_blocks = MovableBlocks(game=self)
        self.insert_blocks()

        self.next_color = random.choice(list(blocks.keys()))
        self.line_broken = 0
        self.score = 0
        # var stores the normal speed, when k up isn't pressed
        self.base_speed = config.data["base_speed"]

        self.over = False

        self.font = pygame.font.SysFont(config.data["font_name"], config.data["font_size"])
        self.counter = 0

        self.key_binds = config.data["key_binds"]

    def insert_blocks(self):
        """""
        insert the moving blocks at the top of the screen
        """""
        y = self.movable_blocks.pos[0] + self.movable_blocks.array.shape[0]
        x = self.movable_blocks.pos[1] + self.movable_blocks.array.shape[1]
        # if there's a put block where the blocks must generate
        for color_value in range(config.data["first_fixed_block"], config.data["last_fixed_block"] + 1):
            if color_value in self.a[self.movable_blocks.pos[0]:y, self.movable_blocks.pos[1]:x]:
                self.over = True
        self.a[self.movable_blocks.pos[0]:y, self.movable_blocks.pos[1]:x] = self.movable_blocks.array

    def reset(self):
        """""
        resets all var to their original values
        """""
        self.line_broken = 0
        self.score = 0
        self.counter = 0
        self.over = False
        # creating the numpy array
        self.arr_size = (self.playing_screen_size[1] // BlockSize, self.playing_screen_size[0] // BlockSize)
        self.a = np.zeros(self.arr_size)

        self.movable_blocks = MovableBlocks(game=self)
        self.insert_blocks()

    def move_line_down(self, y: int):
        """""
        moves all row above y by one
        """""
        # move all the line higher than y by one block
        for i in range(y + 1):
            if y - i != 0:
                self.a[y - i, :] = self.a[y - i - 1, :]
            else:
                self.a[y - i, :] = config.data["empty"]

    def update_next_block(self):
        next_array = blocks[self.next_color][0]

        for y in range(next_array.shape[0]):
            for x in range(next_array.shape[1]):
                if next_array[y, x] == config.data["moving_block"]:
                    self.screen.blit(blocks_image[self.next_color], (
                        self.playing_screen_size[0] + config.data["sidebar_offset"] + x * BlockSize, 70 + y * BlockSize,
                        BlockSize, BlockSize))

    def update_score(self):
        score_text = self.font.render(f"Score : {self.score}", 1, config.data["colors"]["white"])
        self.screen.blit(score_text, (self.playing_screen_size[0] + config.data["sidebar_offset"], 200))

    def update_texts(self):
        blocks_text = self.font.render("Next block:", 1, config.data["colors"]["white"])
        self.screen.blit(blocks_text, (self.playing_screen_size[0] + config.data["sidebar_offset"], 20))

    def update_displays(self):
        """""
        update the displays on the right side of the screen
        """""
        pygame.draw.rect(self.screen, config.data["colors"]["black"], (
            (self.playing_screen_size[0] + config.data["sidebar_offset"], 0),
            (self.screen.get_width() - self.playing_screen_size[0], self.screen.get_height())))

        self.update_score()
        self.update_texts()
        self.update_next_block()
        # creating the right part of the screen
        pygame.draw.rect(self.screen, config.data["colors"]["blue"],
                         ((self.playing_screen_size[0], 0), (10, self.screen.get_height())))

    def update_blocks(self):
        # updating the blocks
        non_zero = np.argwhere(self.a != 0)
        for y, x in non_zero:
            if self.a[y, x] in range(config.data["first_fixed_block"], config.data["last_fixed_block"] + 1):
                self.screen.blit(blocks_image[int(self.a[y, x])],
                                 (x * BlockSize, y * BlockSize, BlockSize, BlockSize))
            else:
                self.screen.blit(blocks_image[self.movable_blocks.color_value],
                                 (x * BlockSize, y * BlockSize, BlockSize, BlockSize))

    def check_lines(self):
        # checks if a line of a is only made of 2s, if so we move all the lines higher than this line down
        for i in range(self.a.shape[0]):
            if not config.data["empty"] in self.a[i, :] and not config.data["moving_block"] in self.a[i, :]:
                self.line_broken += 1
                self.move_line_down(i)
                if self.line_broken % 10 == 0:
                    self.base_speed += 0.5

    def handle_falling(self):
        """""
        makes the moving blocks fall
        """""
        if self.counter % int(15 / self.movable_blocks.speed) == 0:

            # getting the co of the blocks before moving them
            self.movable_blocks.co = self.movable_blocks.get_co(self.a, True)

            # if the block can move down then it moves down
            if not self.movable_blocks.can_move(0, 1):
                self.movable_blocks.move(0, 1)
            else:

                # if the game is over, we don't add the points
                if not self.over:
                    self.score += config.data["score_per_block"]
                    self.spawn_new_blocks()

    def spawn_new_blocks(self):
        for co in self.movable_blocks.co:
            # creating the put blocks with the blocks color
            self.a[co[0], co[1]] = self.movable_blocks.color_value

        # else, we create new blocks
        self.movable_blocks = MovableBlocks(self, self.next_color)
        self.insert_blocks()
        self.next_color = random.choice(list(blocks.keys()))

    def update(self):

        self.update_blocks()

        self.check_lines()

        self.handle_falling()

        self.update_displays()
