import os

class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color

        value_sign = 1 if color == 'blanco' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.name}-{self.color}.png')
    def add_moves(self, move):
        self.moves.append(move)

class Peon(Piece):

    def __init__(self, color):
        if color == 'blanco':
            self.dir = -1
        else:
            self.dir = 1
        super().__init__('peon', color, 1.0)


class Caballo(Piece):

    def __init__(self, color):
        super().__init__('caballo', color, 3.0)


class Alfil(Piece):

    def __init__(self, color):
        super().__init__('alfil', color, 3.001)


class Torre(Piece):

    def __init__(self, color):
        super().__init__('torre', color, 5.0)


class Reina(Piece):

    def __init__(self, color):
        super().__init__('reina', color, 9.0)


class Rey(Piece):

    def __init__(self, color):
        super().__init__('rey', color, 1000.0)