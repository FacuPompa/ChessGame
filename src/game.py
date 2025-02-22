import pygame

from const import *
from tablero import Board
from arrastre import Drag


class Game:

    def __init__(self):
        self.next_player = 'blanco'
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
                center_x = move.final.col * SQSIZE + SQSIZE // 2
                center_y = move.final.row * SQSIZE + SQSIZE // 2
                radius = SQSIZE // 4 
                
                pygame.draw.circle(surface, '#ff0000', (center_x, center_y), radius)
    
    def next_turn(self):
        self.next_player = 'blanco' if self.next_player == 'negro' else 'negro'