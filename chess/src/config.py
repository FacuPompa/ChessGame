import pygame
from theme import Theme

class Config:

    def __init__(self):
        self.theme = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#dd6262', '#dd6262')
        self.font = pygame.font.SysFont('Liberation Serif', 18, bold=True)