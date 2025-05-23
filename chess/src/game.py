import pygame

from const import *
from tablero import ChessBoard
from arrastre import Drag
from config import Config
from square import Square

class Game:

    def __init__(self):
        self.next_player = 'blanco'
        self.hovered_sqr = None
        self.board = ChessBoard()
        self.drag = Drag()
        self.config = Config()
        self.move_history = []
        self.captured_white_imgs = []
        self.captured_black_imgs = []

    def show_bg(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                # coordenadas números
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    surface.blit(lbl, lbl_pos)
                # coordenadas letras
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_aplhacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
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
        theme = self.config.theme
        if self.drag.dragging:
            piece = self.drag.piece
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.row) % 2 == 0 else theme.moves.dark
                center_x = move.final.col * SQSIZE + SQSIZE // 2
                center_y = move.final.row * SQSIZE + SQSIZE // 2
                radius = SQSIZE // 6
                pygame.draw.circle(surface, '#717171', (center_x, center_y), radius)

    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_action:
            initial = self.board.last_action.initial
            final = self.board.last_action.final
            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self):
        self.next_player = 'blanco' if self.next_player == 'negro' else 'negro'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def reset(self):
        self.__init__()