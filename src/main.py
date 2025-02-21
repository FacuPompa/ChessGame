import pygame
import sys

from const import *
from game import Game

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        drag = self.game.drag
        
        
        while True:
            game.show_bg(screen)
            game.show_pieces(screen)

            if drag.dragging:
                drag.update_blit(screen)

            for event in pygame.event.get():

                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drag.update_mouse(event.pos)

                    clicked_row = drag.mouseY // SQSIZE
                    clicked_col = drag.mouseX // SQSIZE

                    #cuadrado tiene pieza?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        drag.save_initial(event.pos)
                        drag.drag_piece(piece)

                #movimiento mouse
                if event.type == pygame.MOUSEMOTION:
                    if drag.dragging:
                        drag.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_pieces(screen)
                        drag.update_blit(screen)

                #suelto click
                if event.type == pygame.MOUSEBUTTONUP:
                    drag.undrag_piece()

                
                #salir
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.display.update()

main = Main()
main.mainloop()