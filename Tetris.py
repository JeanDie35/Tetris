import pygame
pygame.init()
pygame.font.init()
from game import *
from frames import *
from config import *

config = Config()

Font = pygame.font.SysFont(config.data["font_name"], config.data["font_size"])

clock = pygame.time.Clock()
FPS = config.data["FPS"]

"""""
Careful:
 I used numpy to store the position of every block. Although, axis 1 in numpy arrays is the y axis, axis 2 is the x axis
 The numpy array that stores the position of the blocks is called a, there can be 3 different values:
    0 is when there's no block
    1 is for the blocks that you can move
    2-8 is for the blocks that you can't move anymore, the number depends on the color
"""""


running = True

pygame.display.set_caption(config.data["title"])
screen_size = (config.data["screen_width"], config.data["screen_height"])
screen = pygame.display.set_mode(screen_size)

welcome = Welcome(screen, config)
game = Game(screen, config)
settings = Settings(screen, config, game)
game_over = GameOver(screen, config)

active_frame = welcome


while running:
    active_frame.update()
    pygame.display.flip()

    if active_frame == game and game.over:
        # hiding the game widgets
        screen.fill(config.data["bg_color"])
        active_frame = game_over
        game_over.score = game.score


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # saving all the data
            config.save_file()
            pygame.quit()
            running = False

        if event.type == pygame.KEYDOWN:
            if active_frame == game:

                if event.key == game.key_binds["turn right"] or event.key == game.key_binds["turn left"]:

                    # getting the actual co of the blocks
                    game.movable_blocks.co = game.movable_blocks.get_co(game.a, False)

                    if event.key == game.key_binds["turn right"]:
                        simulate_arr = game.movable_blocks.simulate_right_turn()

                    elif event.key == game.key_binds["turn left"]:
                        simulate_arr = game.movable_blocks.simulate_left_turn()

                    # if it can turn
                    if game.movable_blocks.can_fit(simulate_arr):
                        for y, x in game.movable_blocks.co:
                            game.a[y, x] = 0

                        # updating the array
                        game.movable_blocks.array = simulate_arr
                        # updating co
                        game.movable_blocks.co = game.movable_blocks.get_co(game.a, False)

                        for y, x in game.movable_blocks.co:
                            game.a[y, x] = 1


                if event.key == game.key_binds["right"]:

                    # updating the co before moving
                    game.movable_blocks.co = game.movable_blocks.get_co(game.a, True)

                    # if it can move right, then it moves right
                    if game.movable_blocks.can_move(1, 0):
                        game.movable_blocks.move(1, 0)


                elif event.key == game.key_binds["left"]:

                    # checks if the shape can move left
                    game.movable_blocks.co = game.movable_blocks.get_co(game.a, False)

                    # if it can move left, then it moves left
                    if game.movable_blocks.can_move(-1, 0):
                        game.movable_blocks.move(-1, 0)


                if event.key == game.key_binds["speed up"]:
                    game.movable_blocks.speed = 3*game.base_speed

            elif active_frame == settings:

                for k_selector in settings.key_selectors.items():
                    # if a key selector is selected, its key will be the pressed one
                    if k_selector[1].selected:
                        k_selector[1].change_key(event.key)

        elif event.type == pygame.KEYUP:

            if active_frame == game:
                if event.key == game.key_binds["speed up"]:
                    game.movable_blocks.speed = game.base_speed

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if active_frame == welcome:
                if welcome.play_rect.collidepoint(event.pos):
                    # assigning the chosen keys to game
                    for key in game.key_binds.keys():
                        game.key_binds[key] = settings.get_key_movement(key)
                    active_frame = game
                    # we hide the welcome assets
                    screen.fill(config.data["bg_color"])

                if welcome.settings_rect.collidepoint(event.pos):
                    screen.fill(config.data["bg_color"])
                    active_frame = settings

            elif active_frame == settings:

                if settings.back_rect.collidepoint(event.pos):
                    active_frame = welcome
                    # saving the key binds
                    for nkey in game.key_binds.keys():
                        config.data["key_binds"][nkey] = settings.get_key_movement(nkey)


                    screen.fill(config.data["bg_color"])

                # if the user clicks on a key selector, it becomes selected
                for k_selector in settings.key_selectors.items():
                    if k_selector[1].rect.collidepoint(event.pos):
                        k_selector[1].selected = True
                    else:
                        k_selector[1].selected = False

            elif active_frame == game_over:
                if game_over.back_rect.collidepoint(event.pos):
                    game.reset()
                    active_frame = welcome
                    screen.fill(config.data["bg_color"])

    if active_frame == game:
        game.counter += 1
        
    clock.tick(FPS)