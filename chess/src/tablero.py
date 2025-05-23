from const import *
from square import Square
from pieza import *
from move import Move
import copy

class ChessBoard:

    PEON_CLASS = Peon

    def __init__(self):
        self.grid = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]
        self.squares = self.grid
        self.last_action = None
        self.checkmate = False
        self.stalemate = False
        self._setup_pieces('blanco')
        self._setup_pieces('negro')

    def execute_move(self, piece, action, simulation=False, promotion_choice=None):
        start = action.initial
        end = action.final

        captured_piece = None

        # lógica peón al paso y promoción
        if isinstance(piece, Peon):
            if abs(start.row - end.row) == 2:
                piece.paso = True
            else:
                piece.paso = False

            # comer al paso
            if start.col != end.col and self.grid[end.row][end.col].isempty():
                captured_row = start.row
                captured_piece = self.grid[captured_row][end.col].piece
                self.grid[captured_row][end.col].piece = None
                # mover el peón que captura
                self.grid[end.row][end.col].piece = piece
                self.grid[start.row][start.col].piece = None
                piece.moved = True
                piece.moves.clear()
                self.last_action = action
                for row in self.grid:
                    for sq in row:
                        if isinstance(sq.piece, Peon) and sq.piece is not piece:
                            sq.piece.paso = False
                # Detección de mate/ahogado
                if not simulation:
                    self.checkmate = False
                    self.stalemate = False
                    rival = 'negro' if piece.color == 'blanco' else 'blanco'
                    if self.is_checkmate(rival):
                        self.checkmate = True
                    elif self.is_stalemate(rival):
                        self.stalemate = True
                return

            # promoción 
            if (piece.color == 'blanco' and end.row == 0) or (piece.color == 'negro' and end.row == 7):
                if promotion_choice is None:
                    promotion_choice = 'reina'
                if promotion_choice == 'reina':
                    self.grid[end.row][end.col].piece = Reina(piece.color)
                elif promotion_choice == 'torre':
                    self.grid[end.row][end.col].piece = Torre(piece.color)
                elif promotion_choice == 'alfil':
                    self.grid[end.row][end.col].piece = Alfil(piece.color)
                elif promotion_choice == 'caballo':
                    self.grid[end.row][end.col].piece = Caballo(piece.color)
                self.grid[start.row][start.col].piece = None
                piece = self.grid[end.row][end.col].piece
            else:
                self.grid[end.row][end.col].piece = piece
                self.grid[start.row][start.col].piece = None

        # enroque
        elif isinstance(piece, Rey):
            if abs(start.col - end.col) == 2:
                if end.col == 6:  # enroque corto
                    rook = self.grid[start.row][7].piece
                    self.grid[start.row][5].piece = rook
                    self.grid[start.row][7].piece = None
                elif end.col == 2:  # enroque largo
                    rook = self.grid[start.row][0].piece
                    self.grid[start.row][3].piece = rook
                    self.grid[start.row][0].piece = None
            self.grid[end.row][end.col].piece = piece
            self.grid[start.row][start.col].piece = None

        # movimiento normal para cualquier otra pieza
        else:
            self.grid[end.row][end.col].piece = piece
            self.grid[start.row][start.col].piece = None

        piece.moved = True
        piece.moves.clear()
        self.last_action = action

        for row in self.grid:
            for sq in row:
                if isinstance(sq.piece, Peon) and sq.piece is not piece:
                    sq.piece.paso = False

        # detección de mate/ahogado
        if not simulation:
            self.checkmate = False
            self.stalemate = False
            rival = 'negro' if piece.color == 'blanco' else 'blanco'
            if self.is_checkmate(rival):
                self.checkmate = True
            elif self.is_stalemate(rival):
                self.stalemate = True

    def is_legal_move(self, piece, action):
        return action in piece.moves

    def generate_moves(self, piece, row, col, verify_check=True):
        piece.moves.clear()
        if isinstance(piece, Peon):
            self._pawn_moves(piece, row, col, verify_check)
        elif isinstance(piece, Caballo):
            self._knight_moves(piece, row, col, verify_check)
        elif isinstance(piece, Alfil):
            self._slide_moves(piece, row, col, [(-1, -1), (-1, 1), (1, -1), (1, 1)], verify_check)
        elif isinstance(piece, Torre):
            self._slide_moves(piece, row, col, [(-1, 0), (1, 0), (0, -1), (0, 1)], verify_check)
        elif isinstance(piece, Reina):
            self._slide_moves(piece, row, col, [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)], verify_check)
        elif isinstance(piece, Rey):
            self._king_moves(piece, row, col, verify_check)

    def _pawn_moves(self, pawn, row, col, verify_check):
        direction = -1 if pawn.color == 'blanco' else 1
        start_row = 6 if pawn.color == 'blanco' else 1

        # avance simple
        next_row = row + direction
        if Square.in_range(next_row, col) and self.grid[next_row][col].isempty():
            self._add_move_if_legal(pawn, row, col, next_row, col, verify_check)
            # avance doble
            if row == start_row:
                next_row2 = row + 2 * direction
                if self.grid[next_row2][col].isempty():
                    self._add_move_if_legal(pawn, row, col, next_row2, col, verify_check)

        # capturas
        for dc in [-1, 1]:
            capture_col = col + dc
            if Square.in_range(next_row, capture_col):
                target = self.grid[next_row][capture_col]
                if target.has_rival_piece(pawn.color):
                    self._add_move_if_legal(pawn, row, col, next_row, capture_col, verify_check)

        # peón al paso
        for dc in [-1, 1]:
            adj_col = col + dc
            if Square.in_range(row, adj_col):
                adj_sq = self.grid[row][adj_col]
                if isinstance(adj_sq.piece, Peon) and adj_sq.piece.color != pawn.color and adj_sq.piece.paso:
                    ep_row = row + direction
                    self._add_move_if_legal(pawn, row, col, ep_row, adj_col, verify_check)

    def _knight_moves(self, knight, row, col, verify_check):
        jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in jumps:
            r, c = row + dr, col + dc
            if Square.in_range(r, c):
                target = self.grid[r][c]
                if target.isempty() or target.has_rival_piece(knight.color):
                    self._add_move_if_legal(knight, row, col, r, c, verify_check)

    def _slide_moves(self, piece, row, col, directions, verify_check):
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while Square.in_range(r, c):
                if self.grid[r][c].isempty():
                    self._add_move_if_legal(piece, row, col, r, c, verify_check)
                elif self.grid[r][c].has_rival_piece(piece.color):
                    self._add_move_if_legal(piece, row, col, r, c, verify_check)
                    break
                else:
                    break
                r += dr
                c += dc

    def _king_moves(self, king, row, col, verify_check):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if Square.in_range(r, c) and self.grid[r][c].isempty_rival(king.color):
                    self._add_move_if_legal(king, row, col, r, c, verify_check)
        # enroque
        if not king.moved:
            # corto
            if self._can_castle(row, col, 7):
                self._add_move_if_legal(king, row, col, row, 6, verify_check)
            # largo
            if self._can_castle(row, col, 0):
                self._add_move_if_legal(king, row, col, row, 2, verify_check)

    def _can_castle(self, row, king_col, rook_col):
        rook = self.grid[row][rook_col].piece
        if not isinstance(rook, Torre) or rook.moved:
            return False
        step = 1 if rook_col > king_col else -1
        for c in range(king_col + step, rook_col, step):
            if self.grid[row][c].has_piece():
                return False
        return True

    def _add_move_if_legal(self, piece, r1, c1, r2, c2, verify_check):
        move = Move(Square(r1, c1), Square(r2, c2))
        if verify_check:
            if not self._would_cause_check(piece, move):
                piece.moves.append(move)
        else:
            piece.moves.append(move)

    def _would_cause_check(self, piece, move):
        temp_board = copy.deepcopy(self)
        temp_piece = temp_board.grid[move.initial.row][move.initial.col].piece
        temp_board.execute_move(temp_piece, move, simulation=True)
        # buscar rey propio
        king_sq = None
        for row in temp_board.grid:
            for sq in row:
                if isinstance(sq.piece, Rey) and sq.piece.color == piece.color:
                    king_sq = sq
        if not king_sq:
            return False
        # jaque?
        for row in temp_board.grid:
            for sq in row:
                if sq.has_rival_piece(piece.color):
                    temp_board.generate_moves(sq.piece, sq.row, sq.col, verify_check=False)
                    for m in sq.piece.moves:
                        if m.final.row == king_sq.row and m.final.col == king_sq.col:
                            return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        for row in self.grid:
            for sq in row:
                if sq.has_team(color):
                    self.generate_moves(sq.piece, sq.row, sq.col, verify_check=True)
                    if sq.piece.moves:
                        return False
        return True

    def is_stalemate(self, color):
        if self.is_in_check(color):
            return False
        for row in self.grid:
            for sq in row:
                if sq.has_team(color):
                    self.generate_moves(sq.piece, sq.row, sq.col, verify_check=True)
                    if sq.piece.moves:
                        return False
        return True

    def is_in_check(self, color):
        king_sq = None
        for row in self.grid:
            for sq in row:
                if isinstance(sq.piece, Rey) and sq.piece.color == color:
                    king_sq = sq
                    break
        if not king_sq:
            return False
        for row in self.grid:
            for sq in row:
                if sq.has_rival_piece(color):
                    self.generate_moves(sq.piece, sq.row, sq.col, verify_check=False)
                    for m in sq.piece.moves:
                        if m.final.row == king_sq.row and m.final.col == king_sq.col:
                            return True
        return False

    def _setup_pieces(self, color):
        pawn_row, back_row = (6, 7) if color == 'blanco' else (1, 0)
        for col in range(COLS):
            self.grid[pawn_row][col].piece = Peon(color)
        self.grid[back_row][0].piece = Torre(color)
        self.grid[back_row][1].piece = Caballo(color)
        self.grid[back_row][2].piece = Alfil(color)
        self.grid[back_row][3].piece = Reina(color)
        self.grid[back_row][4].piece = Rey(color)
        self.grid[back_row][5].piece = Alfil(color)
        self.grid[back_row][6].piece = Caballo(color)
        self.grid[back_row][7].piece = Torre(color)