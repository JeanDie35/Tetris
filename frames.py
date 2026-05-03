import pygame
pygame.init()
from config import *

# all the keys that can't work with chr() or ord() function but we still want to be able to bind them
special_keys = {
    pygame.K_RIGHT: "right arrow",
    pygame.K_LEFT: "left arrow",
    pygame.K_UP: "up arrow",
    pygame.K_DOWN: "down arrow"
}

config = Config()

# parent class for all the different frames there's
class Frame:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(config.data["font_name"], config.data["font_size"])

    def update(self):
        pass


# thr frame that will be displayed when you launch the app
class Welcome(Frame):

    def __init__(self, screen):

        super().__init__(screen)
        # the images that will be displayed on this frame
        self.assets = {
            "logo" : pygame.image.load("assets/logo.png"),
            "play": pygame.image.load("assets/play_button.png"),
            "settings": pygame.image.load("assets/settings_button.png"),
        }
        # creating a var for the buttons' rect because it'll be needed when cheking if the mouse is on the button
        self.play_rect = self.assets["play"].get_rect()
        self.play_rect.x, self.play_rect.y = (self.screen.get_width() // 2 - self.assets["play"].get_width() // 2, 3 * self.screen.get_height() // 4 - self.assets["play"].get_width() // 4)

        self.settings_rect = self.assets["settings"].get_rect()
        self.settings_rect.x, self.settings_rect.y = (0, 0)

    def update(self):
        # displays all the elements of the frame
        self.screen.blit(self.assets["logo"], (self.screen.get_width() // 2 - self.assets["logo"].get_width() // 2, self.screen.get_height() // 4 - self.assets["logo"].get_width() // 4))

        self.screen.blit(self.assets["play"], self.play_rect)

        self.screen.blit(self.assets["settings"], self.settings_rect)

# the frame where you can change the key binds
class Settings(Frame):

    def __init__(self, screen, game):
        super().__init__(screen)

        self.game = game
        self.assets = {
            "back" : pygame.image.load("assets/back_button.png"),
        }
        # creating a var for the buttons' rect because it'll be needed when cheking if the mouse is on the button
        self.back_rect = self.assets["back"].get_rect()
        self.back_rect.x, self.back_rect.y = (0, 0)

        # creating a dict to store all the key selectors depending on what key are they bound to
        self.key_selectors = {
        "right": KeySelector(self.screen, config.data["key_binds"]["right"], 65),
        "left": KeySelector(self.screen, config.data["key_binds"]["left"], 155),
        "turn right": KeySelector(self.screen, config.data["key_binds"]["turn right"], 245),
        "turn left": KeySelector(self.screen, config.data["key_binds"]["turn left"], 335),
        "speed up": KeySelector(self.screen, config.data["key_binds"]["speed up"], 425)
        }


    def update(self):
        # displays all the elements of the frame
        self.screen.blit(self.assets["back"], self.back_rect)

        # for each key selector
        for i in range(len(list(self.key_selectors.keys()))):
            # we display a text saying what movement is the key selector bound to
            key_text = self.font.render(list(self.key_selectors.keys())[i], 1, config.data["colors"]["white"])
            self.screen.blit(key_text, (self.screen.get_width() // 2 - key_text.get_width() // 2, 20 + i * 90))

            # displays the key selctor
            self.key_selectors[list(self.key_selectors.keys())[i]].display()

    def get_key_movement(self, movement):
        return self.key_selectors[movement].nkey

# frame when the game is over
class GameOver(Frame):


    def __init__(self, screen):
        super().__init__(screen)
        self.score = 0

        self.assets = {
            "back": pygame.image.load("assets/back_button.png"),
            "victory": pygame.image.load("assets/victory.png")
        }
        # creating a var for the buttons' rect because it'll be needed when cheking if the mouse is on the button
        self.back_rect = self.assets["back"].get_rect()
        self.back_rect.x, self.back_rect.y = (0 + self.back_rect.width // 2, self.screen.get_height() - self.back_rect.height - 20)


        self.best_score = config.data["best_score"]

    def update(self):
        # displays the elements of the frame
        self.best_score = max(self.best_score, self.score)
        best_score_text = self.font.render(f"Best score : {self.best_score}", 1, config.data["colors"]["white"])
        self.screen.blit(best_score_text, (self.screen.get_width() // 2 - best_score_text.get_width() // 2,
                                      self.screen.get_height() // 2 - best_score_text.get_height() // 2))

        score_text = self.font.render(f"Your score : {self.score}", 1, config.data["colors"]["white"])
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2,
                                      3 * self.screen.get_height() // 4 - score_text.get_height() // 2))

        self.screen.blit(self.assets["back"], self.back_rect)

        self.screen.blit(self.assets["victory"], (self.screen.get_width() // 2 - self.assets["victory"].get_width() // 2,
                                      self.screen.get_height() // 4 - self.assets["victory"].get_height() // 4))



class KeySelector:

    def __init__(self, screen, nkey, y):
        self.screen = screen
        self.font = pygame.font.SysFont(config.data["font_name"], config.data["font_size"])

        # the key that it is displaying
        self.nkey = nkey
        self.selected = False
        self.size = (200, 50)
        self.rect = pygame.rect.Rect((self.screen.get_width() // 2 - self.size[0] // 2, y), (self.size))

    def display(self):

        pygame.draw.rect(self.screen, config.data["colors"]["grey"], self.rect)

        key_text = self.font.render(self.get_key(self.nkey), 1, config.data["colors"]["white"])
        self.screen.blit(key_text, (self.rect.x + self.rect.w // 2 - key_text.get_width() // 2, self.rect.y + self.rect.h // 2 - key_text.get_height() // 2))


    def change_key(self, n):
        # we call the get_key method, if the chr() function can't handle the number, it raises an error which is then caught
        # if there's no error, the second will be executed
        try :
            self.get_key(n)
            self.nkey = n
        except ValueError:
            print("You can't use that key, please enter another one")


    def get_key(self, nkey):
        if nkey in special_keys:
            return special_keys[nkey]
        else:
            try:
                return chr(nkey)
            except ValueError:
                print("You can't use this key, please enter anonther one")