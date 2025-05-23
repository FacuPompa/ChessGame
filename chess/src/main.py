import pygame
import sys
import os
from collections import Counter
import pygame.mixer

from const import *
from game import Game
from square import Square
from move import Move

PANEL_X = 800
PANEL_W = 200
MOVES_PANEL_H = 380  

class Main:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH + PANEL_W, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.running = True
        self.scroll_offset = 0

        # sonidos
        self.snd_move = pygame.mixer.Sound('assets/sounds/move.mp3')
        self.snd_capture = pygame.mixer.Sound('assets/sounds/capture.mp3')
        self.snd_check = pygame.mixer.Sound('assets/sounds/check.mp3')

        self.piece_images = {}
        nombres = ['peon', 'torre', 'caballo', 'alfil', 'reina', 'rey']
        colores = ['blanco', 'negro']
        for nombre in nombres:
            for color in colores:
                path = f'assets/images/imgs-80px/{nombre}-{color}.png'
                self.piece_images[(nombre, color)] = pygame.transform.smoothscale(
                    pygame.image.load(path), (24, 24)
                )
        self.piece_images_big = {}
        for nombre in ['reina', 'torre', 'alfil', 'caballo']:
            for color in colores:
                path = f'assets/images/imgs-80px/{nombre}-{color}.png'
                self.piece_images_big[(nombre, color)] = pygame.transform.smoothscale(
                    pygame.image.load(path), (90, 90)
                )

    def draw_gradient_bg(self, color_top, color_bottom):
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH + PANEL_W, y))

    def draw_button(self, rect, text, font, color, hover=False):
        base_color = (60, 60, 60) if not hover else (120, 120, 120)
        pygame.draw.rect(self.screen, base_color, rect, border_radius=18)
        pygame.draw.rect(self.screen, color, rect, 3, border_radius=18)
        txt = font.render(text, True, color)
        self.screen.blit(txt, (rect.x + rect.w//2 - txt.get_width()//2, rect.y + rect.h//2 - txt.get_height()//2))

    def draw_captured_grouped(self, captured_imgs, x, y):
        piezas = []
        for img in captured_imgs:
            for key, val in self.piece_images.items():
                if val == img:
                    piezas.append(key)
                    break
        counter = Counter(piezas)
        for i, ((nombre, color), cantidad) in enumerate(counter.items()):
            img = self.piece_images[(nombre, color)]
            self.screen.blit(img, (x + i*32, y))
            if cantidad > 1:
                font = pygame.font.SysFont('Arial', 18, bold=True)
                txt = font.render(f"x{cantidad}", True, (80, 60, 40))
                self.screen.blit(txt, (x + i*32 + 16, y + 16))

    def draw_side_panel(self, game, end_message=None):
        panel_x = PANEL_X
        panel_w = PANEL_W
        pygame.draw.rect(self.screen, (245, 234, 200), (panel_x, 0, panel_w, HEIGHT))
        font = pygame.font.SysFont('Arial', 26, bold=True)
        small_font = pygame.font.SysFont('Arial', 20)
        txt = font.render("Movimientos", True, (80, 60, 40))
        self.screen.blit(txt, (panel_x + 20, 20))

        moves = getattr(game, "move_history", [])
        move_area = pygame.Rect(panel_x, 60, panel_w, MOVES_PANEL_H)
        pygame.draw.rect(self.screen, (235, 225, 180), move_area)
        max_visible = MOVES_PANEL_H // 28
        total_moves = len(moves)
        scroll = self.scroll_offset
        if total_moves > max_visible:
            scroll = max(0, min(scroll, total_moves - max_visible))
            visible_moves = moves[scroll:scroll+max_visible]
        else:
            scroll = 0
            visible_moves = moves

        for i, move in enumerate(visible_moves):
            if isinstance(move, tuple):
                if len(move) == 5:
                    notation, piece_name, piece_color, promo_img, captured_img = move
                elif len(move) == 4:
                    notation, piece_name, piece_color, promo_img = move
                    captured_img = None
                else:
                    notation, piece_name, piece_color = move
                    promo_img = None
                    captured_img = None
                img = self.piece_images.get((piece_name, piece_color))
                if img:
                    self.screen.blit(img, (panel_x + 20, 68 + i*28))
                move_txt = small_font.render(notation, True, (60, 60, 60))
                self.screen.blit(move_txt, (panel_x + 50, 70 + i*28))
                if promo_img:
                    arrow_txt = small_font.render("=>", True, (60, 60, 60))
                    arrow_x = panel_x + 50 + move_txt.get_width() + 6
                    self.screen.blit(arrow_txt, (arrow_x, 70 + i*28))
                    promo_file = os.path.basename(promo_img)
                    promo_name, promo_color = promo_file.split('.')[0].split('-')
                    promo = self.piece_images.get((promo_name, promo_color))
                    if promo:
                        self.screen.blit(promo, (arrow_x + arrow_txt.get_width() + 2, 68 + i*28))
            else:
                move_txt = small_font.render(str(move), True, (60, 60, 60))
                self.screen.blit(move_txt, (panel_x + 20, 70 + i*28))

        if total_moves > max_visible:
            bar_h = int(MOVES_PANEL_H * max_visible / total_moves)
            bar_y = 60 + int((MOVES_PANEL_H-bar_h) * scroll / (total_moves-max_visible))
            pygame.draw.rect(self.screen, (180, 180, 180), (panel_x + panel_w - 12, 60, 8, MOVES_PANEL_H), border_radius=4)
            pygame.draw.rect(self.screen, (120, 120, 120), (panel_x + panel_w - 12, bar_y, 8, bar_h), border_radius=4)

        y_capt = 60 + MOVES_PANEL_H + 20
        self.screen.blit(font.render("Capturas", True, (80, 60, 40)), (panel_x + 20, y_capt))
        xw = panel_x + 20
        yw = y_capt + 40
        xb = panel_x + 20
        yb = yw + 40
        self.draw_captured_grouped(getattr(game, "captured_white_imgs", []), xw, yw)
        self.draw_captured_grouped(getattr(game, "captured_black_imgs", []), xb, yb)

        turn_font = pygame.font.SysFont('Arial', 22, bold=True)
        if not end_message:
            turno = game.next_player.capitalize()
            color_circle = (255,255,255) if game.next_player == "blanco" else (40,40,40)
            pygame.draw.circle(self.screen, color_circle, (panel_x + 30, 670), 14)
            turn_txt = turn_font.render(f"Turno: {turno}", True, (80, 60, 40))
            self.screen.blit(turn_txt, (panel_x + 55, 658))

        btn_font = pygame.font.SysFont('Arial', 22, bold=True)
        btn_w = 140
        btn_h = 40
        btn_x = panel_x + (panel_w - btn_w)//2
        self.restart_btn = pygame.Rect(btn_x, 700, btn_w, btn_h)
        self.menu_btn = pygame.Rect(btn_x, 750, btn_w, btn_h)
        self.draw_button(self.restart_btn, "Jugar otra partida", btn_font, (165, 117, 80))
        self.draw_button(self.menu_btn, "Menú", btn_font, (165, 117, 80))

    def draw_end_message_overlay(self, message):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120)) 
        self.screen.blit(overlay, (0, 0))
        font = pygame.font.SysFont('Arial', 48, bold=True)
        txt = font.render(message, True, (255, 80, 80))
        shadow = font.render(message, True, (0, 0, 0))
        x = WIDTH//2 - txt.get_width()//2
        y = HEIGHT//2 - txt.get_height()//2
        self.screen.blit(shadow, (x+2, y+2))
        self.screen.blit(txt, (x, y))

    def show_start_menu(self):
        font = pygame.font.SysFont('Georgia', 64, bold=True)
        btn_font = pygame.font.SysFont('Arial', 36, bold=True)
        credit_font = pygame.font.SysFont('Arial', 22, italic=True)
        color = (165, 117, 80)
        color_top = (235, 209, 166)
        color_bottom = (165, 117, 80)
        buttons = [
            {"rect": pygame.Rect((WIDTH+PANEL_W)//2-120, 320, 240, 60), "text": "Jugar"},
            {"rect": pygame.Rect((WIDTH+PANEL_W)//2-120, 400, 240, 60), "text": "Instrucciones"},
            {"rect": pygame.Rect((WIDTH+PANEL_W)//2-120, 480, 240, 60), "text": "Salir"},
        ]
        while True:
            self.draw_gradient_bg(color_top, color_bottom)
            title = font.render("Un juego de ajedrez", True, color)
            self.screen.blit(title, ((WIDTH+PANEL_W)//2 - title.get_width()//2, 140))
            mx, my = pygame.mouse.get_pos()
            for btn in buttons:
                hover = btn["rect"].collidepoint(mx, my)
                self.draw_button(btn["rect"], btn["text"], btn_font, color, hover)
            credit = credit_font.render("Creado por Facundo Pompa", True, (80, 60, 40))
            self.screen.blit(credit, ((WIDTH+PANEL_W)//2 - credit.get_width()//2, HEIGHT - 40))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, btn in enumerate(buttons):
                        if btn["rect"].collidepoint(event.pos):
                            if i == 0:
                                return
                            elif i == 1:
                                self.show_instructions()
                            elif i == 2:
                                pygame.quit()
                                sys.exit()

    def show_instructions(self):
        font = pygame.font.SysFont('Arial', 32)
        btn_font = pygame.font.SysFont('Arial', 28, bold=True)
        credit_font = pygame.font.SysFont('Arial', 22, italic=True)
        color = (165, 117, 80)
        color_top = (235, 209, 166)
        color_bottom = (165, 117, 80)
        btn_rect = pygame.Rect((WIDTH+PANEL_W)//2-100, 600, 200, 50)
        lines = [
            "¿Cómo jugar?",
            "- Arrastrá y soltá las piezas para moverlas.",
            "- Hacé clic en una pieza para ver sus movimientos.",
            "- Pulsá 'R' para reiniciar la partida.",
            "- Pulsá 'Salir' para cerrar el juego.",
        ]
        while True:
            self.draw_gradient_bg(color_top, color_bottom)
            for i, line in enumerate(lines):
                txt = font.render(line, True, (255, 255, 255))
                self.screen.blit(txt, ((WIDTH+PANEL_W)//2 - txt.get_width()//2, 120 + i*40))
            mx, my = pygame.mouse.get_pos()
            hover = btn_rect.collidepoint(mx, my)
            self.draw_button(btn_rect, "Volver", btn_font, color, hover)
            credit = credit_font.render("Creado por Facundo Pompa", True, (80, 60, 40))
            self.screen.blit(credit, ((WIDTH+PANEL_W)//2 - credit.get_width()//2, HEIGHT - 40))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_rect.collidepoint(event.pos):
                        return

    def show_promotion_menu(self, color):
        font = pygame.font.SysFont('Arial', 36, bold=True)
        credit_font = pygame.font.SysFont('Arial', 22, italic=True)
        color_top = (235, 209, 166)
        color_bottom = (165, 117, 80)
        options = ['reina', 'torre', 'alfil', 'caballo']
        piece_imgs = [self.piece_images_big[(name, color)] for name in options]
        alpha = 0
        clock = pygame.time.Clock()
        while True:
            self.draw_gradient_bg(color_top, color_bottom)
            overlay = pygame.Surface((WIDTH+PANEL_W, HEIGHT))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            if alpha < 255:
                alpha += 10
            txt = font.render("Elige pieza para promoción", True, (80, 60, 40))
            txt.set_alpha(alpha)
            self.screen.blit(txt, ((WIDTH+PANEL_W)//2 - txt.get_width()//2, 120))
            mx, my = pygame.mouse.get_pos()
            for i, img in enumerate(piece_imgs):
                x = (WIDTH+PANEL_W)//2 - 210 + i*140
                y = HEIGHT//2 - 60
                rect = pygame.Rect(x-10, y-10, 110, 110)
                hover = rect.collidepoint(mx, my)
                border_color = (255, 215, 0) if hover else (180, 180, 180)
                pygame.draw.rect(self.screen, border_color, rect, 4, border_radius=18)
                self.screen.blit(img, (x, y))
            credit = credit_font.render("Creado por Facundo Pompa", True, (80, 60, 40))
            self.screen.blit(credit, ((WIDTH+PANEL_W)//2 - credit.get_width()//2, HEIGHT - 40))
            pygame.display.update()
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(4):
                        x = (WIDTH+PANEL_W)//2 - 210 + i*140
                        y = HEIGHT//2 - 60
                        rect = pygame.Rect(x-10, y-10, 110, 110)
                        if rect.collidepoint(event.pos):
                            return options[i]

    def mainloop(self):
        self.show_start_menu()
        screen = self.screen
        game = self.game
        board = self.game.board
        drag = self.game.drag

        end_message = None
        game_over = False

        while self.running:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            self.draw_side_panel(game, end_message if game_over else None)

            if drag.dragging:
                drag.update_blit(screen)

            if not game_over and board.checkmate:
                end_message = "¡Jaque mate! Ganaron las " + ("blancas" if game.next_player == "negro" else "negras")
                game_over = True
            elif not game_over and board.stalemate:
                end_message = "¡Tablas!"
                game_over = True

            if game_over and end_message:
                self.draw_end_message_overlay(end_message)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEWHEEL:
                    moves = getattr(game, "move_history", [])
                    max_visible = MOVES_PANEL_H // 28
                    total_moves = len(moves)
                    if total_moves > max_visible:
                        self.scroll_offset -= event.y
                        self.scroll_offset = max(0, min(self.scroll_offset, total_moves - max_visible))
                    else:
                        self.scroll_offset = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(self, 'restart_btn') and self.restart_btn.collidepoint(event.pos):
                        game.reset()
                        board = self.game.board
                        drag = self.game.drag
                        self.scroll_offset = 0
                        end_message = None
                        game_over = False
                        continue
                    if hasattr(self, 'menu_btn') and self.menu_btn.collidepoint(event.pos):
                        self.show_start_menu()
                        game.reset()
                        board = self.game.board
                        drag = self.game.drag
                        self.scroll_offset = 0
                        end_message = None
                        game_over = False
                        continue

                    if not game_over:
                        drag.update_mouse(event.pos)
                        clicked_row = drag.mouseY // SQSIZE
                        clicked_col = drag.mouseX // SQSIZE

                        if 0 <= clicked_row < ROWS and 0 <= clicked_col < COLS:
                            if board.squares[clicked_row][clicked_col].has_piece():
                                piece = board.squares[clicked_row][clicked_col].piece
                                if piece.color == game.next_player:
                                    board.generate_moves(piece, clicked_row, clicked_col, verify_check=True)
                                    drag.save_initial(event.pos)
                                    drag.drag_piece(piece)
                                    game.show_bg(screen)
                                    game.show_moves(screen)
                                    game.show_pieces(screen)

                if event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    if 0 <= motion_row < ROWS and 0 <= motion_col < COLS:
                        game.set_hover(motion_row, motion_col)
                    else:
                        game.hovered_sqr = None

                    if drag.dragging:
                        drag.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        self.draw_side_panel(game, end_message if game_over else None)
                        if game_over and end_message:
                            self.draw_end_message_overlay(end_message)
                        drag.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if drag.dragging and not game_over:
                        drag.update_mouse(event.pos)
                        realased_row = drag.mouseY // SQSIZE
                        realased_col = drag.mouseX // SQSIZE

                        if 0 <= realased_row < ROWS and 0 <= realased_col < COLS:
                            initial = Square(drag.initial_row, drag.initial_col)
                            final = Square(realased_row, realased_col)
                            move = Move(initial, final)


                            if board.is_legal_move(drag.piece, move):
                                captured_piece = None
                                captured_img = None
                                is_capture = False

                                if board.squares[final.row][final.col].has_piece():
                                    captured = board.squares[final.row][final.col].piece
                                    if captured and captured.color != drag.piece.color:
                                        captured_piece = captured.name
                                        captured_img = f'assets/images/imgs-80px/{captured.name}-{captured.color}.png'
                                        is_capture = True

                                castling = None
                                if drag.piece.name == "rey" and abs(final.col - initial.col) == 2:
                                    castling = "O-O" if final.col > initial.col else "O-O-O"

                                promotion = None
                                promo_img = None
                                if isinstance(drag.piece, board.PEON_CLASS):
                                    if (drag.piece.color == 'blanco' and final.row == 0) or (drag.piece.color == 'negro' and final.row == 7):
                                        promotion = self.show_promotion_menu(drag.piece.color)
                                        promo_img = f'assets/images/imgs-80px/{promotion}-{drag.piece.color}.png'
                                        board.execute_move(drag.piece, move, promotion_choice=promotion)
                                    else:
                                        board.execute_move(drag.piece, move)
                                else:
                                    board.execute_move(drag.piece, move)

                                check = ""
                                if board.checkmate:
                                    check = "#"
                                elif board.is_in_check(game.next_player):
                                    check = "+"

                                # sonidos
                                if is_capture:
                                    self.snd_capture.play()
                                elif check == "+":
                                    self.snd_check.play()
                                else:
                                    self.snd_move.play()

                                if castling:
                                    notation = castling + check
                                else:
                                    from_sq = f"{Square.get_aplhacol(initial.col)}{8-initial.row}"
                                    to_sq = f"{Square.get_aplhacol(final.col)}{8-final.row}"
                                    if captured_piece:
                                        notation = f"{from_sq}x{to_sq}"
                                    else:
                                        notation = f"{from_sq}-{to_sq}"
                                    if promotion:
                                        notation += ""
                                    notation += check

                                game.move_history.append((notation, drag.piece.name, drag.piece.color, promo_img, captured_img))

                                if captured_piece and captured_img:
                                    img = self.piece_images.get((captured_piece, captured.color))
                                    if img:
                                        if captured.color == 'blanco':
                                            game.captured_white_imgs.append(img)
                                        else:
                                            game.captured_black_imgs.append(img)
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                game.next_turn()
                        drag.undrag_piece()
                    else:
                        drag.undrag_piece()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                        board = self.game.board
                        drag = self.game.drag
                        self.scroll_offset = 0
                        end_message = None
                        game_over = False

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.mainloop()