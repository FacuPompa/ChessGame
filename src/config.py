import pygame


from theme import Theme

class Config:

    def __init__(self):
        self.themes = []
        self.add_themes()
        self.index = 0
        self.theme = self.themes[self.index]
        self.font = pygame.font.SysFont('Liberation Serif', 18, bold=True)
        

    def change_theme (self):
        self.index +=1
        self.index %= len(self.themes)
        self.theme = self.themes[self.index]

    def add_themes(self):
        madera = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#dd6262', '#dd6262')
        chess = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#dd6262', '#dd6262')
        blanco_negro = Theme((255, 255, 255), (52, 52, 52), (82, 102, 128), (80, 80, 80), '#dd6262', '#dd6262')
        azul = Theme((220, 230, 245), (50, 90, 140), (123, 187, 227), (43, 119, 191), '#dd6262', '#dd6262')
        rojo = Theme((180, 50, 50), (90, 20, 20), (200, 80, 80), (120, 40, 40), '#dd6262', '#dd6262')

        self.themes = [madera, chess, blanco_negro, azul, rojo]