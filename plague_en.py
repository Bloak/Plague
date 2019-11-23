import pygame
import socket
import pickle
from modules import Player
from modules import Game
from modules import Data
from modules import Button
from modules import Chess

server = '172.104.19.177'
port = 5555

Black = (0, 0, 0)
White = (255, 255, 255)
Grey = (128, 128, 128)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

pygame.init()

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Plague')

fps = 60

pygame.font.init()
default_font = pygame.font.get_default_font()


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(fps)
        win.fill(White)
        button1 = Button(default_font, 60, 'Click to Start', Black, None, ('mid_width', 'mid_height'), width, height)
        button1.draw(win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if button1.click(event):
                run = False

    main()


def main():
    run = True
    clock = pygame.time.Clock()
    network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        network.connect((server, port))
    except socket.error as e:
        print(e)
        print('No connection')
        run = False

    if run:
        player = pickle.loads(network.recv(2048 * 32))  # receive player info
        your_id = player.in_game_id
        hand = player.hand
        color = player.color
        print(your_id)
        print(hand)
        print(color)

    while run:
        clock.tick(fps)

        network.sendall(pickle.dumps(Data('normal')))  # default report

        try:
            game = pickle.loads(network.recv(2048 * 32))  # receive game
        except:
            print('fail to receive game')
            continue

        if game.players[your_id].access:
            win.fill(White)
        else:
            win.fill(Grey)

        if game.ready:
            for chess in game.board:  # draw board
                game.board[chess].draw(win)

            red_count, blue_count = game.count_chess()  # show scores
            button9 = Button(default_font, 40, 'Score', Black, None, (10, 10), width, height)
            button9.draw(win)
            button4 = Button(default_font, 40, str(red_count), Red, None, (10, 60), width, height)
            button4.draw(win)
            button5 = Button(default_font, 40, str(blue_count), Blue, None, (10, 110), width, height)
            button5.draw(win)

            button10 = Button(default_font, 40, 'Step', Black, None, (400, 10), width, height)  # show steps
            button10.draw(win)
            button7 = Button(default_font, 40, str(game.players[0].step + game.players[0].extra_step),
                             game.players[0].color, None, (450, 60), width, height)
            button7.draw(win)
            button8 = Button(default_font, 40, str(game.players[1].step + game.players[1].extra_step),
                             game.players[1].color, None, (450, 110), width, height)
            button8.draw(win)

            button6 = Button(default_font, 30, 'End Turn', White, Black, (10, 460), width, height)  # end turn button
            if game.players[your_id].access:
                button6.draw(win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if game.players[your_id].access:
                    for chess in game.board:  # 操作检测
                        if game.board[chess].click(event):
                            print(color)
                            print(game.board[chess].color)
                            print(game.board[chess].new)
                            if game.board[chess].color is None:
                                print(chess, 'operate')
                                network.sendall(pickle.dumps(Data([chess, 'operate'])))  # report location of move
                                break
                            elif (game.board[chess].color == color) and (game.board[chess].new is True):
                                print(chess, 'cancel')
                                network.sendall(pickle.dumps(Data([chess, 'cancel'])))  # report location of erase
                            else:
                                print(chess, 'invalid')
                                network.sendall(pickle.dumps(Data([chess, 'invalid'])))  # report invalid operation

                    if event.type == pygame.KEYDOWN:  # end turn through Enter
                        if event.key == pygame.K_RETURN:
                            network.sendall(pickle.dumps(Data('end turn')))

                    if button6.click(event):  # end turn through click
                        network.sendall(pickle.dumps(Data('end turn')))

        elif game.exist:  # waiting screen
            button2 = Button(default_font, 40, 'Waiting for Player', Black, None, ('mid_width', 200), width, height)
            button2.draw(win)
            button3 = Button(default_font, 40, 'Click to Return', Black, None, ('mid_width', 260), width, height)
            button3.draw(win)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if button2.click(event) or button3.click(event):
                    run = False
        else:
            run = False
            break

        pygame.display.update()


while True:
    menu_screen()