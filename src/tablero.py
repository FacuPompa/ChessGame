from const import *
from square import Square
from pieza import *
from move import Move

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._create()
        self._add_pieces('blanco')
        self._add_pieces('negro')
      

    def calc_moves(self, piece, row, col):

        def peon_moves():
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                pass

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
        
        if isinstance(piece, Peon): peon_moves()
        elif isinstance (piece, Caballo): caballo_moves()
        elif isinstance (piece, Alfil): pass
        elif isinstance (piece, Torre): pass
        elif isinstance (piece, Reina): pass
        elif isinstance (piece, Rey): pass

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