from const import *
from square import Square
from pieza import *

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._create()
        self._add_pieces('blanco')
        self._add_pieces('negro')
      
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