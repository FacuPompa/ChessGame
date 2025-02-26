import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

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
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)


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

                        #pieza de color válida ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            drag.save_initial(event.pos)
                            drag.drag_piece(piece)

                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)


                #movimiento mouse
                if event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    
                    game.set_hover(motion_row, motion_col)

                    if drag.dragging:
                        drag.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        drag.update_blit(screen)

                #suelto click
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if drag.dragging:
                        drag.update_mouse(event.pos)

                        realased_row = drag.mouseY // SQSIZE
                        realased_col = drag.mouseX // SQSIZE

                        #crea posible movimiento
                        initial = Square(drag.initial_row, drag.initial_col)
                        final = Square(realased_row, realased_col)
                        move = Move(initial, final)
                    
                        #movimiento válido ?
                        if board.valid_move(drag.piece, move):
                            board.move(drag.piece, move)


                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                        #siguiente turno
                            game.next_turn()

                    drag.undrag_piece()


                #tecla

                elif event.type == pygame.KEYDOWN:
                    
                    #cambiar el color del tema
                    if event.key == pygame.K_f:  
                        game.change_theme()

                    #reseteando
                    if event.key == pygame.K_r:  
                        game.reset()
                        game = self.game
                        board = self.game.board
                        drag = self.game.drag


                #salir
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.display.update()

main = Main()
main.mainloop()