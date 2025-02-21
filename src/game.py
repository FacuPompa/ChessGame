import pygame

from const import *
from tablero import Board
from arrastre import Drag


class Game:

    def __init__(self):
        self.board = Board()
        self.drag = Drag()


#muestra de methods

    def show_bg(self, surface):
        for row in range (ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (220, 188, 146) #blancas
                else:
                    color = (176, 109, 59)  #negras

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range (ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.drag.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.drag.dragging:
            piece = self.drag.piece

            for move in piece.moves:
                color = '#C84646' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
