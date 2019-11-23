import pygame
import math

Black = (0, 0, 0)
White = (255, 255, 255)
Grey = (128, 128, 128)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)


class Player:
    def __init__(self, id):
        self.exist = True
        self.id = id
        self.in_game = None
        self.in_game_id = None
        self.hand = None
        self.color = None
        self.access = False
        self.step = 0
        self.extra_step = 0


class Game:
    def __init__(self, id):
        self.exist = True
        self.id = id
        self.players = []
        self.ready = False
        self.board = None

    def add_player(self, player):
        self.players.append(player)
        player.in_game = self.id

    def count_player(self):
        return len(self.players)

    def create_board(self, size, screen_width, screen_height):
        self.board = {}
        for row in range(size * 2 - 1):
            for column in range(size * 2 - 1 - abs(row + 1 - size)):
                self.board[(row + 1, column + 1)] = Chess(size, screen_width, screen_height, row + 1, column + 1)

    def count_chess(self):
        red_count = blue_count = 0
        for chess in self.board:
            if self.board[chess].color == Red:
                red_count += 1
            elif self.board[chess].color == Blue:
                blue_count += 1
        return red_count, blue_count

    def count_step(self, chess_pos, color):
        step = 100
        chess = self.board[chess_pos]
        chess.counted = True
        neighbor_chess1 = []
        for other_chess in self.board:
            if chess.neighbor(self.board[other_chess]) and (self.board[other_chess].counted is False) and (
                    self.board[other_chess].color is None or self.board[other_chess].color == color):
                self.board[other_chess].counted = True
                neighbor_chess1.append(self.board[other_chess])
                if (chess.color == self.board[other_chess].color) and (self.board[other_chess].new is False):
                    step = 1
                    break
        if step == 100:
            neighbor_chess2 = []
            for chess1 in neighbor_chess1:
                for other_chess in self.board:
                    if chess1.neighbor(self.board[other_chess]) and (self.board[other_chess].counted is False) and (
                            self.board[other_chess].color is None or self.board[other_chess].color == color):
                        self.board[other_chess].counted = True
                        neighbor_chess2.append(self.board[other_chess])
                        if (chess.color == self.board[other_chess].color) and (self.board[other_chess].new is False):
                            step = 2
                            break
                if step != 100:
                    break
        if step == 100:
            neighbor_chess3 = []
            for chess2 in neighbor_chess2:
                for other_chess in self.board:
                    if chess2.neighbor(self.board[other_chess]) and (self.board[other_chess].counted is False) and (
                            self.board[other_chess].color is None or self.board[other_chess].color == color):
                        self.board[other_chess].counted = True
                        neighbor_chess3.append(self.board[other_chess])
                        if (chess.color == self.board[other_chess].color) and (self.board[other_chess].new is False):
                            step = 3
                            break
                if step != 100:
                    break
        if step == 100:
            for chess3 in neighbor_chess3:
                for other_chess in self.board:
                    if chess3.neighbor(self.board[other_chess]) and (self.board[other_chess].counted is False) and (
                            self.board[other_chess].color is None or self.board[other_chess].color == color):
                        if (chess.color == self.board[other_chess].color) and (self.board[other_chess].new is False):
                            step = 4
                            break
                if step != 100:
                    break

        for chess in self.board:
            self.board[chess].counted = False

        return step


class Data:
    def __init__(self, content):
        self.content = content


class Button:
    def __init__(self, font, size, content, text_color, background_color, pos, screen_width, screen_height):
        self.font = pygame.font.SysFont(font, size)
        self.width, self.height = self.font.size(content)
        self.content = content
        self.text_color = text_color
        self.background_color = background_color
        self.text = self.font.render(content, 1, self.text_color, self.background_color)
        if pos[0] == 'mid_width':
            self.x = screen_width / 2 - self.width / 2
        else:
            self.x = pos[0]
        if pos[1] == 'mid_height':
            self.y = screen_height / 2 - self.height / 2
        else:
            self.y = pos[1]
        self.pos = (self.x, self.y)

    def draw(self, win):
        win.blit(self.text, self.pos)

    def click(self, event):
        click = False
        if event.type == pygame.MOUSEBUTTONUP:
            cursor = pygame.mouse.get_pos()
            if (self.pos[0] < cursor[0] < self.pos[0] + self.width) and (
                    self.pos[1] < cursor[1] < self.pos[1] + self.height):
                click = True

        return click


class Chess:
    def __init__(self, board_size, screen_width, screen_height, row, column):
        self.size = board_size
        self.row = row
        self.column = column
        self.color = None
        self.new = None
        self.step_return = 0
        self.extra_step_return = 0
        self.radius = screen_width / (self.size * 2 - 1) / 2
        self.y = screen_height / 2 + (self.row - self.size) * self.radius * math.sqrt(3)
        self.x = self.radius * (1 + abs(self.row - self.size) + 2 * (self.column - 1))
        self.counted = False

    def new_color(self):
        if self.color == Red:
            new_color = (255, 130, 71)
        elif self.color == Blue:
            new_color = (0, 191, 255)
        else:
            new_color = None
        return new_color

    def draw(self, win):
        if self.color is None:
            pygame.draw.circle(win, Black, (int(self.x), int(self.y)), 5, 0)
        elif self.new is False:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), int(self.radius), 0)
        elif self.new is True:
            pygame.draw.circle(win, self.new_color(), (int(self.x), int(self.y)), int(self.radius), 0)

    def click(self, event):
        click = False
        if event.type == pygame.MOUSEBUTTONUP:
            cursor = pygame.mouse.get_pos()
            if math.sqrt(((self.x - cursor[0]) ** 2) + ((self.y - cursor[1]) ** 2)) < self.radius:
                click = True

        return click

    def neighbor(self, chess):
        neighbor = False
        if self.row == chess.row:
            if (self.column == chess.column + 1) or (self.column == chess.column - 1):
                neighbor = True
        elif self.row == chess.row + 1:
            if self.row <= self.size:
                if (self.column == chess.column) or (self.column == chess.column + 1):
                    neighbor = True
            else:
                if (self.column == chess.column) or (self.column == chess.column - 1):
                    neighbor = True
        elif self.row == chess.row - 1:
            if chess.row <= self.size:
                if (self.column == chess.column) or (self.column == chess.column - 1):
                    neighbor = True
            else:
                if (self.column == chess.column) or (self.column == chess.column + 1):
                    neighbor = True

        return neighbor
