import pygame
pygame.init()
import numpy as np
import random

BlockSize = 25

# dic stores all the arrays for each type of block, with the rotated ones too
blocks = {
    2: [np.array([[0, 1, 0], [1, 1, 0], [0, 1, 0]]), np.array([[0, 0, 0], [1, 1, 1], [0, 1, 0]]), np.array([[0, 1, 0], [0, 1, 1], [0, 1, 0]]), np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]])],
    3: [np.array([[1, 0, 0], [1, 1, 0], [0, 1, 0]]), np.array([[0, 0, 0], [0, 1, 1], [1, 1, 0]]), np.array([[0, 1, 0], [0, 1, 1], [0, 0, 1]]), np.array([[0, 1, 1], [1, 1, 0]])],
    4: [np.array([[0, 1, 0], [0, 1, 0], [1, 1, 0]]), np.array([[0, 0, 0], [1, 1, 1], [0, 0, 1]]), np.array([[0, 1, 1], [0, 1, 0], [0, 1, 0]]), np.array([[1, 0, 0], [1, 1, 1]])],
    5: [np.array([[1, 1, 0], [0, 1, 0], [0, 1, 0]]), np.array([[0, 0, 0], [1, 1, 1], [1, 0 , 0]]), np.array([[0, 1, 0], [0, 1, 0], [0, 1, 1]]), np.array([[0, 0, 1], [1, 1, 1]])],
    6: [np.array([[0, 1], [0, 1], [0, 1], [0, 1]]), np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1]]), np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]), np.array([[0, 0, 0, 0], [1, 1, 1, 1]])],
    7: [np.array([[1, 1], [1, 1]]), np.array([[1, 1], [1, 1]]), np.array([[1, 1], [1, 1]]), np.array([[1, 1], [1, 1]])],
    8: [np.array([[0, 1, 0], [1, 1, 0], [1, 0, 0]]), np.array([[0, 0, 0], [1, 1, 0], [0, 1, 1]]), np.array([[0, 0, 1], [0, 1, 1], [0, 1, 0]]), np.array([[1, 1, 0], [0, 1, 1]])]
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

    def __init__(self, game, color=random.choices(list(blocks.keys()))[0]):
        self.speed = 1
        self.color_value = color
        self.state = 0
        self.array = blocks[self.color_value][self.state]
        self.put = False
        self.movable = True
        self.game = game
        # we get the coordinates of each block of the movable_blocks
        self.co = self.get_co(self.game.a, True)
        # stores the actual positon of the array, so when it turns, it doesn't move right
        self.pos = [0, self.game.playing_screen_size[0] // 2 // BlockSize]

    def get_co(self, array, reverse):
        arr_co = np.nonzero(array == 1)
        # we sort the list with the biggest co in the first place so when we make the blocks go down 1 block they don't destroy each other
        # you must reverse it or not depending on where the block will move, to understand this better make a scheme
        return sorted(list(zip(arr_co[0], arr_co[1])), reverse=reverse)

    def turn_right(self):
        self.state += 1
        if self.state >= 4:
            self.state = 0

    def turn_left(self):
        self.state -= 1
        if self.state <= -1:
            self.state = 3

    def update_array(self):
        self.array = blocks[self.color_value][self.state]

    def move_down(self):
        self.pos[0] += 1
        for i in range(len(self.co)):
            # hiding the old block
            self.game.a[self.co[i][0], self.co[i][1]] = 0
            self.game.a[self.co[i][0] + 1, self.co[i][1]] = 1

    def move_left(self):
        self.pos[1] -= 1
        for i in range(len(self.co)):
            # hiding the old blocks
            self.game.a[self.co[i][0], self.co[i][1]] = 0
            self.game.a[self.co[i][0], self.co[i][1] - 1] = 1

    def move_right(self):
        self.pos[1] += 1
        for i in range(len(self.co)):
            # hide the old blocks
            self.game.a[self.co[i][0], self.co[i][1]] = 0
            self.game.a[self.co[i][0], self.co[i][1] + 1] = 1

class Game:

    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.playing_screen_size = (self.config.data["playing_screen_width"], self.config.data["playing_screen_height"])
        # creating the numpy array
        self.arr_size = (self.playing_screen_size[1] // BlockSize, self.playing_screen_size[0] // BlockSize)
        self.a = np.zeros(self.arr_size)

        self.movable_blocks = MovableBlocks(game=self)
        self.insert_blocks()

        self.next_color = random.choices(list(blocks.keys()))[0]
        self.line_broken = 0
        self.score = 0
        # var stores the normal speed, when k up isn't pressed
        self.normal_speed = self.config.data["normal_speed"]

        self.offset = 20

        self.over = False

        self.font = pygame.font.SysFont(self.config.data["font_name"], self.config.data["font_size"])
        self.counter = 0

        self.key_binds = self.config.data["key_binds"]

    def insert_blocks(self):
        y = self.movable_blocks.pos[0] + self.movable_blocks.array.shape[0]
        x = self.movable_blocks.pos[1] + self.movable_blocks.array.shape[1]
        # if there's a put block where the blocks must generate
        for color_value in range(2, 9):
            if color_value in self.a[self.movable_blocks.pos[0]:y, self.movable_blocks.pos[1]:x]:
                self.over = True
        self.a[self.movable_blocks.pos[0]:y, self.movable_blocks.pos[1]:x] = self.movable_blocks.array

    def reset(self):
        self.line_broke = 0
        self.score = 0
        self.counter = 0
        self.over = False
        # creating the numpy array
        self.arr_size = (self.playing_screen_size[1] // BlockSize, self.playing_screen_size[0] // BlockSize)
        self.a = np.zeros(self.arr_size)

        self.movable_blocks = MovableBlocks(game=self)
        self.insert_blocks()

    def move_line_down(self, y):
        # move all the line higher than y by one block
        for i in range(y + 1):
            if y - i != 0:
                self.a[y - i, :] = self.a[y - i - 1, :]
            else:
                self.a[y - i, :] = 0

    def update_next_block(self):
        next_array = blocks[self.next_color][0]

        for y in range(next_array.shape[0]):
            for x in range(next_array.shape[1]):
                if next_array[y, x] == 1:
                    self.screen.blit(blocks_image[self.next_color], (
                    self.playing_screen_size[0] + self.offset + x * BlockSize, 70 + y * BlockSize, BlockSize, BlockSize))

    def update_score(self):
        score_text = self.font.render(f"Score : {self.score}", 1, (255, 255, 255))
        self.screen.blit(score_text, (self.playing_screen_size[0] + self.offset, 200))

    def update_texts(self):
        blocks_text = self.font.render("Next block:", 1, (255, 255, 255))
        self.screen.blit(blocks_text, (self.playing_screen_size[0] + self.offset, 20))

    def update_displays(self):
        pygame.draw.rect(self.screen, [0, 0, 0], ((self.playing_screen_size[0] + self.offset, 0), (self.screen.get_width() - self.playing_screen_size[0], self.screen.get_height())))
        self.update_score()
        self.update_texts()
        self.update_next_block()
        # creating the right part of the screen
        pygame.draw.rect(self.screen, [0, 0, 255], ((self.playing_screen_size[0], 0), (10, self.screen.get_height())))

    def update(self):
        # updating the blocks
        for y in range(self.a.shape[0]):
            for x in range(self.a.shape[1]):
                if self.a[y, x] == 1:
                    self.screen.blit(blocks_image[self.movable_blocks.color_value],
                                (x * BlockSize, y * BlockSize, BlockSize, BlockSize))
                elif self.a[y, x] == 0:
                    pygame.draw.rect(self.screen, [0, 0, 0], (x * BlockSize, y * BlockSize, BlockSize, BlockSize))
                else:
                    self.screen.blit(blocks_image[int(self.a[y, x])], (x * BlockSize, y * BlockSize, BlockSize, BlockSize))

        # checks if a line of a is only made of 2s, if so we move all the lines higher than this line down
        for i in range(self.a.shape[0]):
            if not 0 in self.a[i, :] and not 1 in self.a[i, :]:
                self.line_broken += 1
                self.move_line_down(i)
                if self.line_broken % 10 == 0:
                    self.normal_speed += 0.5

        if self.counter % int(15 / self.movable_blocks.speed) == 0:

            # getting the co of the blocks before moving them
            self.movable_blocks.co = self.movable_blocks.get_co(self.a, True)

            # checks if the blocks can move down
            for i in range(len(self.movable_blocks.co)):
                # checks if the block below is not a put block or the end of the screen                                                     range(2, 9) correspond to all the possible values for a put block
                if self.movable_blocks.co[i][0] + 1 >= self.playing_screen_size[1] // BlockSize or self.a[
                    self.movable_blocks.co[i][0] + 1, self.movable_blocks.co[i][1]] in range(2, 9):
                    self.movable_blocks.put = True
                    break

            # if the block can move down then it moves down
            if not self.movable_blocks.put:
                self.movable_blocks.move_down()
            else:
                # else, we create new blocks
                for co in self.movable_blocks.co:
                    # creating the put blocks with the blocks color
                    self.a[co[0], co[1]] = self.movable_blocks.color_value

                self.movable_blocks = MovableBlocks(self, self.next_color)
                self.insert_blocks()
                self.next_color = random.choices(list(blocks.keys()))[0]
                if not self.over:
                    self.score += 4


        self.update_displays()