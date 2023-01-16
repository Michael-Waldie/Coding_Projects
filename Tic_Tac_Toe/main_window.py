import PySimpleGUI as sg

sg.theme('DarkAmber')
import Tic_Tac_Toe

layout = [
    [sg.Text('Enter first player\'s name:'),
     sg.Input('Player One', key='-FIRST_PLAYER-', do_not_clear=True, size=(20, 1))],
    [sg.Text('Enter second player\'s name:'),
     sg.Input('Player Two', key='-SECOND_PLAYER-', do_not_clear=True, size=(20, 1))],
    [sg.Button('Start Game')]
]

window = sg.Window('Tic Tac Toe', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    elif event == 'Start Game':
        players = [values['-FIRST_PLAYER-'], values['-SECOND_PLAYER-']]
        Tic_Tac_Toe.initiate_game(players)
