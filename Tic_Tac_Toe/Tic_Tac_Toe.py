import PySimpleGUI as sg

sg.theme('DarkAmber')


def check_if_winner(board):
    for column in range(0, 3):
        # print(board)
        if ((0, column) in board.keys()) and ((1, column) in board.keys()) and ((2, column) in board.keys()):
            if board[(0, column)] == board[(1, column)] == board[(2, column)]:
                return board[(0, column)]

    for row in range(0, 3):
        if ((row, 0) in board.keys()) and ((row, 1) in board.keys()) and ((row, 2) in board.keys()):
            if board[(row, 0)] == board[(row, 1)] == board[(row, 2)]:
                return board[(row, 0)]

    if ((0, 0) in board.keys()) and ((1, 1) in board.keys()) and ((2, 2) in board.keys()):
        if board[(0, 0)] == board[(1, 1)] == board[(2, 2)]:
            return board[(1, 1)]

    if ((2, 0) in board.keys()) and ((1, 1) in board.keys()) and ((0, 2) in board.keys()):
        if board[(2, 0)] == board[(1, 1)] == board[(0, 2)]:
            return board[(2, 0)]


def disable_board(window, boolval):
    for row in range(3):
        for col in range(3):
            window[(row, col)].update(disabled=boolval)


def initiate_game(players):
    board, player, timer = {}, 0, 0
    pone, ptwo = 0, 0

    layout = [[sg.Text('Current Player: ' + players[player], key='-CURRENT_PLAYER-')],

              [sg.Button(size=(3, 2), key=(0, 0)), sg.Button(size=(3, 2), key=(0, 1)),
               sg.Button(size=(3, 2), key=(0, 2)), sg.Text('Score:')],

              [sg.Button(size=(3, 2), key=(1, 0)), sg.Button(size=(3, 2), key=(1, 1)),
               sg.Button(size=(3, 2), key=(1, 2)), sg.Text('Player One: ' + '0', key='-FIRST_SCORE-')],

              [sg.Button(size=(3, 2), key=(2, 0)), sg.Button(size=(3, 2), key=(2, 1)),
               sg.Button(size=(3, 2), key=(2, 2)), sg.Text('Player Two: ' + '0', key='-SECOND_SCORE-')],

              [sg.Button('Reset Board'), sg.Button('Clear Score'), sg.Button('Cancel')]]

    window = sg.Window('Tic Tac Toe', layout, use_default_focus=False)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break

        if event == 'Reset Board':
            board = {}
            for row in range(3):
                for col in range(3):
                    window[(row, col)].update('')
            disable_board(window, False)
            timer = 0

        elif event == 'Clear Score':
            print(pone, ptwo)
            pone, ptwo = 0, 0
            window['-FIRST_SCORE-'].update('Player One: ' + '0')
            window['-SECOND_SCORE-'].update('Player Two: ' + '0')
            print(pone, ptwo)

        elif event not in board:
            board[event] = player
            window[event].update('X' if player else '0')
            is_winner = check_if_winner(board)

            if is_winner is not None:
                sg.popup('           The winner is ' + players[player] + '.           ', title='Tic Tac Toe')
                if player == 0:
                    pone += 1
                    window['-FIRST_SCORE-'].update('Player One: ' + str(pone))
                else:
                    ptwo += 1
                    window['-SECOND_SCORE-'].update('Player Two: ' + str(ptwo))
                disable_board(window, True)

            elif timer == 8:
                sg.popup('           Game ends in draw.           ', title='Tic Tac Toe')
                disable_board(window, True)

            player = (player + 1) % 2
            timer += 1
            print(timer)
            window['-CURRENT_PLAYER-'].update('Current player: ' + players[player])

    window.close()
