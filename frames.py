import pygame
pygame.init()

class Frame:

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def update(self):
        pass



class Welcome(Frame):

    def __init__(self, screen, font: pygame.font.Font):

        super().__init__(screen, font)
        self.assets = {
            "logo" : pygame.image.load("assets/logo.png"),
            "play": pygame.image.load("assets/play_button.png"),
            "settings": pygame.image.load("assets/settings_button.png"),
        }
        self.play_rect = self.assets["play"].get_rect()
        self.play_rect.x, self.play_rect.y = (self.screen.get_width() // 2 - self.assets["play"].get_width() // 2, 3 * self.screen.get_height() // 4 - self.assets["play"].get_width() // 4)

        self.settings_rect = self.assets["settings"].get_rect()
        self.settings_rect.x, self.settings_rect.y = (0, 0)

    def update(self):
        self.screen.blit(self.assets["logo"], (self.screen.get_width() // 2 - self.assets["logo"].get_width() // 2, self.screen.get_height() // 4 - self.assets["logo"].get_width() // 4))

        self.screen.blit(self.assets["play"], self.play_rect)

        self.screen.blit(self.assets["settings"], self.settings_rect)


class Settings(Frame):

    def __init__(self, screen, font: pygame.font.Font, game):
        super().__init__(screen, font)

        self.game = game
        self.assets = {
            "back" : pygame.image.load("assets/back_button.png"),
        }
        self.back_rect = self.assets["back"].get_rect()
        self.back_rect.x, self.back_rect.y = (0, 0)


    def update(self):
        self.screen.blit(self.assets["back"], self.back_rect)

class GameOver(Frame):

    def __init__(self, screen, font):
        super().__init__(screen, font)
        self.score = 0

        self.assets = {
            "back": pygame.image.load("assets/back_button.png"),
            "victory": pygame.image.load("assets/victory.png")
        }
        self.back_rect = self.assets["back"].get_rect()
        self.back_rect.x, self.back_rect.y = (0 + self.back_rect.width // 2, self.screen.get_height() - self.back_rect.height - 20)

        file = open("best_score.txt", "r")
        self.best_score = int(file.readlines()[0])
        file.close()

    def update(self):

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
