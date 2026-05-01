import pygame
pygame.init()
pygame.font.init()
from game import *
from frames import *

BgColor = [0, 0, 0]
Font = pygame.font.SysFont("Comic Sans MS", 25)

clock = pygame.time.Clock()
FPS = 60

"""""
Careful:
 I used numpy to store the position of every block. Although, axis 1 in numpy arrays is the y axis, axis 2 is the x axis
 The numpy array that stores the position of the blocks is called a, there can be 3 different values:
    0 is when there's no block
    1 is for the blocks that you can move
    2-8 is for the blocks that you can't move anymore, the number depends on the color
"""""


running = True

pygame.display.set_caption("Tetris")
screen_size = (500, 600)
screen = pygame.display.set_mode(screen_size)

welcome = Welcome(screen, Font)
game = Game(screen, Font)
settings = Settings(screen, Font, game)
game_over = GameOver(screen, Font)

active_frame = welcome

while running:

    active_frame.update()

    if active_frame == game and game.over:
        # hiding the game widgets
        screen.fill("black")
        active_frame = game_over
        game_over.score = game.score


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False

        if event.type == pygame.KEYDOWN:
            if active_frame == game:

                if event.key == game.key_binds["turn right"] or event.key == game.key_binds["turn left"]:

                    # getting the actual co of the blocks
                    game.movable_blocks.co = game.movable_blocks.get_co(game.a, False)

                    if event.key == game.key_binds["turn right"]:
                        game.movable_blocks.turn_right()

                    elif event.key == game.key_binds["turn left"]:
                        game.movable_blocks.turn_left()


                    game.movable_blocks.update_array()
                    # getting the new co of the blocks, after turning
                    new_co = game.movable_blocks.get_co(game.movable_blocks.array, False)

                    for i in range(len(new_co)):
                        # calculates the co  of the new blocks on the main array a
                        new_co[i] = (new_co[i][0] + game.movable_blocks.pos[0], new_co[i][1] + game.movable_blocks.pos[1])
                        # checks if the blocks can turn without hitting put blocks or going out of the screen
                        if 0 > new_co[i][0] or new_co[i][0] >= game.playing_screen_size[1] // BlockSize or 0 > new_co[i][1] or new_co[i][1] >= game.playing_screen_size[0] // BlockSize or game.a[new_co[i]] in range(2, 9):
                            game.movable_blocks.movable = False

                    if game.movable_blocks.movable:
                        # hide the old blocks
                        for n in game.movable_blocks.co:
                            game.a[n] = 0
                        for i in range(len(new_co)):
                            game.a[new_co[i]] = 1
                    game.movable_blocks.movable = True

                if event.key == game.key_binds["right"]:

                    # checking if the shape can move right
                    game.movable_blocks.co = game.movable_blocks.get_co(game.a, True)

                    for i in range(len(game.movable_blocks.co)):
                        # checks if the block on the right is not a put block or the end of the screen
                        if game.movable_blocks.co[i][1] + 1 >= game.playing_screen_size[0] // BlockSize or game.a[game.movable_blocks.co[i][0], game.movable_blocks.co[i][1] + 1] in range(2, 9):
                            game.movable_blocks.movable = False
                            break

                    # if it can move right, then it moves right
                    if game.movable_blocks.movable:
                        game.movable_blocks.move_right()

                    game.movable_blocks.movable = True

                elif event.key == game.key_binds["left"]:

                    # checks if the shape can move left
                    game.movable_blocks.co = game.movable_blocks.get_co(game.a, False)

                    for i in range(len(game.movable_blocks.co)):
                        # checks if the block on the right is not a put block or the end of the screen
                        if game.movable_blocks.co[i][1] - 1 == -1 or game.a[game.movable_blocks.co[i][0], game.movable_blocks.co[i][1] - 1] in range(2, 9):
                            game.movable_blocks.movable = False
                            break

                    # if it can move left, then it moves left
                    if game.movable_blocks.movable:
                        game.movable_blocks.move_left()

                    game.movable_blocks.movable = True

                if event.key == game.key_binds["speed up"]:
                    game.movable_blocks.speed = 3*game.normal_speed

            elif active_frame == settings:

                for k_selector in settings.key_selectors.items():
                    # if a key selector is selected, its key will be the pressed one
                    if k_selector[1].selected:
                        k_selector[1].change_key(event.key)

        elif event.type == pygame.KEYUP:

            if active_frame == game:
                if event.key == game.key_binds["speed up"]:
                    game.movable_blocks.speed = game.normal_speed

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if active_frame == welcome:
                if welcome.play_rect.collidepoint(event.pos):
                    # assigning the chosen keys to game
                    for key in game.key_binds.keys():
                        game.key_binds[key] = settings.get_key(key)
                    active_frame = game
                    # we hide the welcome assets
                    screen.fill("black")

                if welcome.settings_rect.collidepoint(event.pos):
                    screen.fill("black")
                    active_frame = settings

            elif active_frame == settings:

                if settings.back_rect.collidepoint(event.pos):
                    active_frame = welcome
                    screen.fill("black")

                # if the user clicks on a key selector, it becomes selected
                for k_selector in settings.key_selectors.items():
                    if k_selector[1].rect.collidepoint(event.pos):
                        k_selector[1].selected = True
                    else:
                        k_selector[1].selected = False

            elif active_frame == game_over:
                if game_over.back_rect.collidepoint(event.pos):
                    game_over.save_best_score()
                    game.reset()
                    active_frame = welcome
                    screen.fill("black")

    if active_frame == game:
        game.counter += 1

    pygame.display.flip()
    clock.tick(FPS)