import pygame
pygame.init()
import numpy as np
import random

BlockSize = 25
BgColor = [0, 0, 0]
Shapes = [np.array([1, 1, 1, 1]), np.array([[1, 0], [1, 1], [1, 0]]), np.array([[0, 1], [1, 1], [0, 1]]), np.array([[1, 1], [1, 1]]), np.array([[0, 1], [1, 1], [1, 0]]), np.array([[1, 0], [1, 1], [0, 1]]), np.array([[1,1], [1, 0], [1, 0]]), np.array([[1,1], [0, 1], [0, 1]])]

clock = pygame.time.Clock()
FPS = 60

"""""
Careful:
 I used numpy to store the position of every block. Although, axis 1 in numpy arrays is the y axis, axis 2 is the x axis
 The numpy array that stores the position of the blocks is called a, there can be 3 different values:
    0 is when there's no block
    1 is for the blocks that you can move
    2 is for the blocks that you can't move anymore
"""""

# dic stores all the arrays for each type of block, with the rotated ones too
blocks = {
    "blue": [np.array([[0, 1, 0], [1, 1, 0], [0, 1, 0]]), np.array([[0, 0, 0], [1, 1, 1], [0, 1, 0]]), np.array([[0, 1, 0], [0, 1, 1], [0, 1, 0]]), np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]])],
    "cyan": [np.array([[1, 0, 0], [1, 1, 0], [0, 1, 0]]), np.array([[0, 0, 0], [0, 1, 1], [1, 1, 0]]), np.array([[0, 1, 0], [0, 1, 1], [0, 0, 1]]), np.array([[0, 1, 1], [1, 1, 0]])],
    "green": [np.array([[0, 1, 0], [0, 1, 0], [1, 1, 0]]), np.array([[0, 0, 0], [1, 1, 1], [0, 0, 1]]), np.array([[0, 1, 1], [0, 1, 0], [0, 1, 0]]), np.array([[1, 0, 0], [1, 1, 1]])],
    "pink": [np.array([[1, 1, 0], [0, 1, 0], [0, 1, 0]]), np.array([[0, 0, 0], [1, 1, 1], [1, 0 , 0]]), np.array([[0, 1, 0], [0, 1, 0], [0, 1, 1]]), np.array([[0, 0, 1], [1, 1, 1]])],
    "purple": [np.array([[0, 1], [0, 1], [0, 1], [0, 1]]), np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1]]), np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]), np.array([[0, 0, 0, 0], [1, 1, 1, 1]])],
    "red": [np.array([[1, 1], [1, 1]]), np.array([[1, 1], [1, 1]]), np.array([[1, 1], [1, 1]]), np.array([[1, 1], [1, 1]])],
    "yellow": [np.array([[0, 1, 0], [1, 1, 0], [1, 0, 0]]), np.array([[0, 0, 0], [1, 1, 0], [0, 1, 1]]), np.array([[0, 0, 1], [0, 1, 1], [0, 1, 0]]), np.array([[1, 1, 0], [0, 1, 1]])]
}

blocks_image = {
    "blue": pygame.transform.scale(pygame.image.load("assets/blue_block.png"), (BlockSize, BlockSize)),
    "cyan": pygame.transform.scale(pygame.image.load("assets/cyan_block.png"), (BlockSize, BlockSize)),
    "green": pygame.transform.scale(pygame.image.load("assets/green_block.png"), (BlockSize, BlockSize)),
    "pink": pygame.transform.scale(pygame.image.load("assets/pink_block.png"), (BlockSize, BlockSize)),
    "purple": pygame.transform.scale(pygame.image.load("assets/purple_block.png"), (BlockSize, BlockSize)),
    "red": pygame.transform.scale(pygame.image.load("assets/red_block.png"), (BlockSize, BlockSize)),
    "yellow": pygame.transform.scale(pygame.image.load("assets/yellow_block.png"), (BlockSize, BlockSize)),
}

class MovableBlocks:

    def __init__(self):
        self.speed = 1
        self.color = random.choices(list(blocks.keys()))[0]
        self.state = 0
        self.array = blocks[self.color][self.state]
        self.put = False
        self.movable = True
        # we get the coordinates of each block of the movable_blocks
        self.co = self.get_co(a, True)
        # stores the actual positon of the array, so when it turns, it doesn't move right
        self.pos = [0, screen_size[0] // 2 // BlockSize]

    def get_co(self, array, reverse):
        arr_co = np.nonzero(array == 1)
        # we sort the list with the biggest co in the first place so when we make the blocks go down 1 block they don't destroy each other
        # you must reverse it or not depending on where the block will move, to understand this better make a scheme
        return sorted(list(zip(arr_co[0], arr_co[1])), reverse=reverse)

    def turn(self):
        self.state += 1
        if self.state >= 4:
            self.state = 0

    def update_array(self):
        self.array = blocks[self.color][self.state]

    def move_down(self):
        self.pos[0] += 1
        for i in range(len(self.co)):
            # hiding the old block
            a[self.co[i][0], self.co[i][1]] = 0
            a[self.co[i][0] + 1, self.co[i][1]] = 1

    def move_left(self):
        self.pos[1] -= 1
        for i in range(len(self.co)):
            # hiding the old blocks
            a[self.co[i][0], self.co[i][1]] = 0
            a[self.co[i][0], self.co[i][1] - 1] = 1

    def move_right(self):
        self.pos[1] += 1
        for i in range(len(self.co)):
            # hide the old blocks
            a[self.co[i][0], self.co[i][1]] = 0
            a[self.co[i][0], self.co[i][1] + 1] = 1



def insert_blocks():

    y = movable_blocks.pos[0] + movable_blocks.array.shape[0]
    x = movable_blocks.pos[1] + movable_blocks.array.shape[1]
    # if there's a put block where the blocks must generate
    if 2 in a[movable_blocks.pos[0]:y, movable_blocks.pos[1]:x]:
        pygame.quit()
        running = False
    else:
        a[movable_blocks.pos[0]:y, movable_blocks.pos[1]:x] = movable_blocks.array


def move_line_down(y):
    # move all the line higher than y by one block
    for i in range(y + 1):
        if y - i != 0:
            a[y - i, :] = a[y - i - 1, :]
        else:
            a[y - i, :] = 0



running = True

pygame.display.set_caption("Tetris")
screen_size = (250, 600)
screen = pygame.display.set_mode(screen_size)

#creating the numpy array
arr_size = (screen_size[1] // BlockSize, screen_size[0] // BlockSize)
a = np.zeros(arr_size)

movable_blocks = MovableBlocks()
insert_blocks()

# c is a counter of the number of iterations of the main loop
c = 0

while running:


    # updating the blocks
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if a[y, x] == 1:
                screen.blit(blocks_image[movable_blocks.color], (x*BlockSize, y*BlockSize, BlockSize, BlockSize))
            elif a[y, x] == 0:
                pygame.draw.rect(screen, [0, 0, 0], (x*BlockSize, y*BlockSize, BlockSize, BlockSize))

    # checks if a line of a is only made of 2s, if so we move all the lines higher than this line down
    for i in range(a.shape[0]):
        if not 0 in a[i, :] and not 1 in a[i, :]:
            move_line_down(i)

    if c % int(15/movable_blocks.speed) == 0:

        # getting the co of the blocks before moving them
        movable_blocks.co = movable_blocks.get_co(a, True)

        # checks if the blocks can move down
        for i in range(len(movable_blocks.co)):
            # checks if the block below is not a put block or the end of the screen
            if movable_blocks.co[i][0] + 1 >= screen_size[1] // BlockSize or a[movable_blocks.co[i][0] + 1, movable_blocks.co[i][1]] == 2:
                movable_blocks.put = True
                break

        # if the block can move down then it moves down
        if not movable_blocks.put:
            movable_blocks.move_down()
        else:
            # else, we create new blocks
            a[a==1] = 2
            movable_blocks = MovableBlocks()
            insert_blocks()

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:

                # getting the actual co of the blocks
                movable_blocks.co = movable_blocks.get_co(a, False)

                movable_blocks.turn()
                movable_blocks.update_array()
                # getting the new co of the blocks, after turning
                new_co = movable_blocks.get_co(movable_blocks.array, False)

                for i in range(len(new_co)):
                    # calculates the co  of the new blocks on the main array a
                    new_co[i] = (new_co[i][0] + movable_blocks.pos[0], new_co[i][1] + movable_blocks.pos[1])
                    # checks if the blocks can turn without hitting put blocks or going out of the screen
                    if 0 > new_co[i][0] or new_co[i][0] >= screen_size[1] // BlockSize or 0 > new_co[i][1] or new_co[i][1] >= screen_size[0] // BlockSize or a[new_co[i]] == 2:
                        movable_blocks.movable = False

                if movable_blocks.movable:
                    # hide the old blocks
                    for n in movable_blocks.co:
                        a[n] = 0
                    for i in range(len(new_co)):
                        a[new_co[i]] = 1
                movable_blocks.movable = True

            elif event.key == pygame.K_RIGHT:

                # checking if the shape can move right
                movable_blocks.co = movable_blocks.get_co(a, True)

                for i in range(len(movable_blocks.co)):
                    # checks if the block on the right is not a put block or the end of the screen
                    if movable_blocks.co[i][1] + 1 >= screen_size[0] // BlockSize or a[movable_blocks.co[i][0], movable_blocks.co[i][1]+1] == 2:
                        print("yes")
                        movable_blocks.movable = False
                        break

                # if it can move right, then it moves right
                if movable_blocks.movable:
                    movable_blocks.move_right()

                movable_blocks.movable = True

            elif event.key == pygame.K_LEFT:

                # checks if the shape can move left
                movable_blocks.co = movable_blocks.get_co(a, False)

                for i in range(len(movable_blocks.co)):
                    # checks if the block on the right is not a put block or the end of the screen
                    if movable_blocks.co[i][1] - 1 == -1 or a[movable_blocks.co[i][0], movable_blocks.co[i][1] - 1] == 2:
                        movable_blocks.movable = False
                        break

                # if it can move left, then it moves left
                if movable_blocks.movable:
                    movable_blocks.move_left()

                movable_blocks.movable = True

            elif event.key == pygame.K_DOWN:
                movable_blocks.speed = 3

        else:
            movable_blocks.speed = 1

    c += 1
    clock.tick(FPS)