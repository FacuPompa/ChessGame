from const import *
from square import Square
from pieza import *
from move import Move

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('blanco')
        self._add_pieces('negro')
      

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        #actualiza el movimiento en el tablero
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        #mueve
        piece.moved = True

        #limpia movimiento valido
        piece.clear_moves()

        #setea ultimo movimiento
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):

        def peon_moves():
            steps = 1 if piece.moved else 2

            #movimiento vertical
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))                           #checkear lógica
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
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
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
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
                        final = Square(possible_move_row, possible_move_col)

                        move = Move(initial, final)
                        piece.add_move(move)
        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)

                        if self.squares[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)

                        if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break

                        if self.squares[possible_move_row][possible_move_col].has_team(piece.color):
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
                        piece.add_move(move)
            
            #enroque

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