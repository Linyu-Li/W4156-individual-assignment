import sqlite3
from sqlite3 import Error
#from flask import request
from Gameboard import Gameboard


'''
Initializes the Table GAME
Do not modify
'''

gameboard = None


def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE GAME(current_turn TEXT, board TEXT,' +
                     'winner TEXT, player1 TEXT, player2 TEXT' +
                     ', remaining_moves INT)')
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
move is a tuple (current_turn, board, winner, player1, player2,
remaining_moves)
Insert Tuple into table
'''


def add_move(move):  # will take in a tuple
    conn = None
    '''
    global gameboard
    gameboard = Gameboard()
    ct = gameboard.current_turn
    board = gameboard.board
    winner = gameboard.game_result
    p1 = gameboard.player1
    p2 = gameboard.player2
    rm = gameboard.remaining_moves
    '''
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('INSERT INTO GAME VALUES ' + str(move))
        print('add_move finished')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close() 


'''
Get the last move played
return (current_turn, board, winner, player1, player2, remaining_moves)
'''


def getMove():
    # will return tuple(current_turn, board, winner, player1, player2,
    # remaining_moves) or None if db fails
    conn = None
    global gameboard
    gameboard = Gameboard()
    remainin_moves = gameboard.remaining_moves
    try:
        conn = sqlite3.connect('sqlite_db')
        exect = conn.execute('SELECT * FROM GAME WHERE remaining_moves = ' + 
                            str(remainin_moves))

        res = None                    
        for row in exect:
            res = (row[0], row[1], row[2], row[3], row[4], row[5])
        
        print("getMove finished")
        return res
        
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
Clears the Table GAME
Do not modify
'''


def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE GAME")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
