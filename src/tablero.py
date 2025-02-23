from const import *
from square import Square
from pieza import *
from move import Move
import copy

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('blanco')
        self._add_pieces('negro')
      

    def move(self, piece, move, testing = False):
        initial = move.initial
        final = move.final

        peon_al_paso = self.squares[final.row][final.col].isempty()

        #actualiza el movimiento
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece



        # resetear el estado "paso" de todos los peones antes de actualizar el nuevo
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Peon):
                    self.squares[row][col].piece.paso = False  

        #marcar si el peon movió dos casillas
        if isinstance(piece, Peon):
            if abs(initial.row - final.row) == 2: 
                piece.paso = True
            else:
                self.check_promotion(piece, final)

            if isinstance(piece, Peon):

                    #peon al paso comer
                diff = final.col - initial.col
                if diff != 0 and peon_al_paso:
                    self.squares[initial.row][initial.col + diff].piece = None
                    self.squares[final.row][final.col].piece = piece

                #peón al paso
                if self.peon_al_paso(initial, final):
                    piece.paso = True
                
                #coronación de peón
                else:
                    self.check_promotion(piece, final)

        #enroque

        if isinstance(piece, Rey):
            if self.enroque(initial, final) and not testing:
                diff = final.col - initial.col
                torre = piece.torre_izquierda if (diff < 0) else piece.torre_derecha
                self.move(torre, torre.moves[-1])

        #mueve
        piece.moved = True

        #limpia movimiento valido
        piece.clear_moves()

        #setea ultimo movimiento
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Reina(piece.color)

    def enroque(self, initial, final):
        return abs(initial.col - final.col ) == 2
    
    def peon_al_paso(self, initial, final):
        return abs(initial.row - final.row) == 2
    
    def peon_al_paso_capturado(self):
        pass
    def jaque(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing = True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, Rey):
                            return True
        return False

    def calc_moves(self, piece, row, col, bool=True): #movimientos posibles de todas las piezas

        def peon_moves():
            steps = 1 if piece.moved else 2

            #movimiento vertical
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)

                        #chekea jaque
                        if bool:
                            if not self.jaque(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else: break#bloqueado 
                else: break#sin rango

            #movimiento diagonal
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                #chekea jaque
                        if bool:
                            if not self.jaque(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            #movimiento peon al paso
            r = 3 if piece.color == 'blanco' else 4
            fr = 2 if piece.color == 'blanco' else 5

            # izquierda
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_rival_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Peon):
                        if p.paso:
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            move = Move(initial, final)
                            
                            # jaque ?
                            if bool:
                                if not self.jaque(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
            
            # derecha
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_rival_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Peon):
                        if p.paso:
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            move = Move(initial, final)
                            
                            # jaque ?
                            if bool:
                                if not self.jaque(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
       
        def caballo_moves():
            possible_moves = [
                (row-2, col +1),
                (row-1, col +2),
                (row+1, col +2),
                (row+2, col +1),
                (row+2, col -1),
                (row+1, col -2),
                (row-1, col -2),
                (row-2, col -1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range (possible_move_row, possible_move_col):
                    if self.squares[possible_move_row] [possible_move_col].isempty_rival(piece.color):

                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                    #chekea jaque
                        if bool:
                            if not self.jaque(piece, move):
                                piece.add_move(move)
                            else:break
                        else:
                            piece.add_move(move)
        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #chekea jaque
                            if bool:
                                if not self.jaque(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        #chekea jaque
                            if bool:
                                if not self.jaque(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                                break

                        elif self.squares[possible_move_row][possible_move_col].has_team(piece.color):
                            break
                    
                    else: break

                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def rey_moves():
            adjs = [
                (row-1, col+0), #arriba
                (row-1, col+1), #arriba derecha
                (row+1, col+1), #derecha
                (row+1, col+1), #abajo derecha
                (row+1, col+0), #abajo
                (row-1, col-1), #abajo izquierda
                (row+0, col-1), #izquierda
                (row-1, col-1), #arriba izquierda
            ]

            #movimiento normal

            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        #chekea jaque
                        if bool:
                            if not self.jaque(piece, move):
                                piece.add_move(move)
                            else: break
                        else:
                            piece.add_move(move)
            
            #enroque
            if not piece.moved:

                torre_derecha = self.squares[row][7].piece
                if isinstance(torre_derecha, Torre):
                    if not torre_derecha.moved:
                        for c in range (5, 7):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 6:
                                piece.torre_derecha = torre_derecha

                                #movimiento torre
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveT = Move(initial, final)

                                #movimiento rey
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveR = Move(initial, final)

                                #chekea jaque
                                if bool:
                                    if not self.jaque(piece, moveR) and not self.jaque(torre_derecha, moveT):
                                        torre_derecha.add_move(moveT)
                                        piece.add_move(moveR)
                                else:
                                    torre_derecha.add_move(moveT)
                                    piece.add_move(move)

        if isinstance(piece, Peon):
            peon_moves()

        elif isinstance (piece, Caballo):

            caballo_moves()
        
        elif isinstance (piece, Alfil): straightline_moves([
            (-1, 1), #arriba derecha 
            (-1, -1), #arriba izquierda
            (1, 1), #abajo derecha
            (1, -1), #abajo izquierda

        ])
        
        elif isinstance (piece, Torre):
            straightline_moves([
                (-1, 0), #arriba
                (0, 1), #derecha
                (1, 0), #abajo
                (0, -1), #izquierda
            ])

        elif isinstance (piece, Reina):
            straightline_moves([
            (-1, 1), #arriba derecha 
            (-1, -1), #arriba izquierda
            (1, 1), #abajo derecha
            (1, -1), #abajo izquierda
            (-1, 0), #arriba
            (0, 1), #derecha
            (1, 0), #abajo
            (0, -1), #izquierda
                
            ])

        elif isinstance (piece, Rey):
            rey_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_peon, row_other = (6, 7) if color == 'blanco' else (1, 0)

        # Peón
        for col in range (COLS):
            self.squares[row_peon][col] = Square(row_peon, col, Peon(color))
            
        # Caballo 
        self.squares[row_other][1] = Square(row_other, 1, Caballo(color))
        self.squares[row_other][6] = Square(row_other, 6, Caballo(color)) 

        # Alfiles
        self.squares[row_other][2] = Square(row_other, 2, Alfil(color))
        self.squares[row_other][5] = Square(row_other, 5, Alfil(color))

        # Torre
        self.squares[row_other][0] = Square(row_other, 0, Torre(color))
        self.squares[row_other][7] = Square(row_other, 7, Torre(color))

        # Reina
        self.squares[row_other][3] = Square(row_other, 3, Reina(color))

        # Rey
        self.squares[row_other][4] = Square(row_other, 4, Rey(color))