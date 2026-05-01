import pygame
pygame.init()

# all the keys that can't work with chr() or ord() function but we still want to be able to bind them
special_keys = {
    pygame.K_RIGHT: "right arrow",
    pygame.K_LEFT: "left arrow",
    pygame.K_UP: "up arrow",
    pygame.K_DOWN: "down arrow"
}

# parent class for all the different frames there's
class Frame:

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def update(self):
        pass


# thr frame that will be displayed when you launch the app
class Welcome(Frame):

    def __init__(self, screen, font: pygame.font.Font):

        super().__init__(screen, font)
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

    def __init__(self, screen, font: pygame.font.Font, game):
        super().__init__(screen, font)

        self.game = game
        self.assets = {
            "back" : pygame.image.load("assets/back_button.png"),
        }
        # creating a var for the buttons' rect because it'll be needed when cheking if the mouse is on the button
        self.back_rect = self.assets["back"].get_rect()
        self.back_rect.x, self.back_rect.y = (0, 0)

        # creating a dict to store all the key selectors depending on what key are they bound to
        self.key_selectors = {
        "right": KeySelector(self.screen, "d", 65, self.font),
        "left": KeySelector(self.screen, "q", 155, self.font),
        "turn right": KeySelector(self.screen, "left arrow", 245, self.font),
        "turn left": KeySelector(self.screen, "right arrow", 335, self.font),
        "speed up": KeySelector(self.screen, "s", 425, self.font)
        }


    def update(self):
        # displays all the elements of the frame
        self.screen.blit(self.assets["back"], self.back_rect)

        # for each key selector
        for i in range(len(list(self.key_selectors.keys()))):
            # we display a text saying what movement is the key selector bound to
            key_text = self.font.render(list(self.key_selectors.keys())[i], 1, [255, 255, 255])
            self.screen.blit(key_text, (self.screen.get_width() // 2 - key_text.get_width() // 2, 20 + i * 90))

            # displays the key selctor
            self.key_selectors[list(self.key_selectors.keys())[i]].display()

    def get_key(self, movement):
        # returns the key that the user chose to bound to movement
        key = 0
        # if the movement is in the special keys
        for item in special_keys.items():
            if item[1] == self.key_selectors[movement].key:
                key = item[0]
        # if the key isn't we can use ord()
        if key == 0:
            key = ord(self.key_selectors[movement].key)
        return key

# frame when the game is over
class GameOver(Frame):


    def __init__(self, screen, font):
        super().__init__(screen, font)
        self.score = 0

        self.assets = {
            "back": pygame.image.load("assets/back_button.png"),
            "victory": pygame.image.load("assets/victory.png")
        }
        # creating a var for the buttons' rect because it'll be needed when cheking if the mouse is on the button
        self.back_rect = self.assets["back"].get_rect()
        self.back_rect.x, self.back_rect.y = (0 + self.back_rect.width // 2, self.screen.get_height() - self.back_rect.height - 20)

        file = open("best_score.txt", "r")
        self.best_score = int(file.readlines()[0])
        file.close()

    def update(self):
        # displays the elements of the frame
        self.best_score = max(self.best_score, self.score)
        best_score_text = self.font.render(f"Best score : {self.best_score}", 1, (255, 255, 255))
        self.screen.blit(best_score_text, (self.screen.get_width() // 2 - best_score_text.get_width() // 2,
                                      self.screen.get_height() // 2 - best_score_text.get_height() // 2))

        score_text = self.font.render(f"Your score : {self.score}", 1, (255, 255, 255))
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2,
                                      3 * self.screen.get_height() // 4 - score_text.get_height() // 2))

        self.screen.blit(self.assets["back"], self.back_rect)

        self.screen.blit(self.assets["victory"], (self.screen.get_width() // 2 - self.assets["victory"].get_width() // 2,
                                      self.screen.get_height() // 4 - self.assets["victory"].get_height() // 4))

    def save_best_score(self):
        file = open("best_score.txt", "w")
        file.write(str(self.best_score))
        file.close()


class KeySelector:

    def __init__(self, screen, key, y, font):
        self.screen = screen
        self.font = font
        # the key that it is displaying
        self.key = key
        self.selected = False
        self.size = (200, 50)
        self.rect = pygame.rect.Rect((self.screen.get_width() // 2 - self.size[0] // 2, y), (self.size))

    def display(self):

        pygame.draw.rect(self.screen, [200, 200, 200], self.rect)

        key_text = self.font.render(str(self.key), 1, [255, 255, 255])
        self.screen.blit(key_text, (self.rect.x + self.rect.w // 2 - key_text.get_width() // 2, self.rect.y + self.rect.h // 2 - key_text.get_height() // 2))


    def change_key(self, n):
        try:
            if n in list(special_keys.keys()):
                self.key = special_keys[n]
            else:
                self.key = chr(n)
        # if the key isn't a letter or an arrow, it will trigger an error because n will be too big for chr() function
        except ValueError:
            print("You can't use that key, please try another one")


