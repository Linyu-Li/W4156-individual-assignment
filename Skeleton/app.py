# import json
from flask import Flask, render_template, request, jsonify
# from flask import redirect


from Gameboard import Gameboard

import db

import logging


app = Flask(__name__)


log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

game = Gameboard()

"""
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
"""


@app.route("/", methods=["GET"])
def player1_connect():
    db.clear()
    db.init_db()

    game.setColorForP1("")
    game.setColorForP2("")
    game.setBoard([[0 for x in range(7)] for y in range(6)])
    game.setCurrentTurn("p1")
    game.setGameResult("")
    game.setReMoves(42)

    return render_template("player1_connect.html", status="Pick a Color.")


"""
Helper function that sends to all boards don't modify
"""


@app.route("/autoUpdate", methods=["GET"])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result, color=game.player1)
    except Exception:
        return jsonify(move="")


"""
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
"""


@app.route("/p1Color", methods=["GET"])
def player1_config():
    if db.getMove() is None:
        color = request.args.get("color", "")
        game.setColorForP1(color)
    else:
        tup = db.getMove()
        board = tup[1].split(".")
        board = board[0: -1]
        board_new = []
        for row in board:
            row = row.replace('[', '').replace(']', '').replace('\\', '').replace('\'', '')
            row = row.split(', ')
            row_new = []
            for i in row:
                if i == '0':
                   i = int(i)
                   row_new.append(i)
                else:
                    row_new.append(i)
            board_new.append(row_new)

        player1 = tup[3]
        player2 = tup[4]
        result = tup[2]
        cu_turn = tup[0]
        re_moves = tup[1]
        game.setColorForP1(player1)
        game.setColorForP2(player2)
        game.setBoard(board_new)
        game.setGameResult(result)
        game.setCurrentTurn(cu_turn)
        game.setReMoves(re_moves)

        return render_template("player1_connect.html", status=game.player1)

    return render_template("player1_connect.html", status=color)


"""
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
"""


@app.route("/p2Join", methods=["GET"])
def p2Join():
    '''
    p1Color = game.player1

    if p1Color == "yellow":
        game.player2 = "red"
        return render_template("p2Join.html", status=game.player2)
    elif p1Color == "red":
        game.player2 = "yellow"
        return render_template("p2Join.html", status=game.player2)
    else:
        return render_template(
            "p2Join.html", status="Error! P1 did not pick color first!"
        )
        '''

    if db.getMove() is None:
        p1Color = game.player1

        if p1Color == "yellow":
            game.player2 = "red"
            return render_template("p2Join.html", status=game.player2)
        elif p1Color == "red":
            game.player2 = "yellow"
            return render_template("p2Join.html", status=game.player2)
        else:
            return render_template(
                "p2Join.html", status="Error! P1 did not pick color first!"
            )
    else:
        tup = db.getMove()
        board = tup[1].split(".")
        board = board[0: -1]
        board_new = []
        for row in board:
            row = row.replace('[', '').replace(']', '').replace('\\', '').replace('\'', '')
            row = row.split(', ')
            row_new = []
            for i in row:
                if i == '0':
                   i = int(i)
                   row_new.append(i)
                else:
                    row_new.append(i)
            board_new.append(row_new)

        player1 = tup[3]
        player2 = tup[4]
        result = tup[2]
        cu_turn = tup[0]
        re_moves = tup[1]
        game.setColorForP1(player1)
        game.setColorForP2(player2)
        game.setBoard(board_new)
        game.setGameResult(result)
        game.setCurrentTurn(cu_turn)
        game.setReMoves(re_moves)

        return render_template("p2Join.html", status=game.player2)


"""
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
"""


@app.route("/move1", methods=["POST"])
def p1_move():
    global game
    col = int(request.get_json()["column"][-1])

    verify = game.verify("p1", col)

    if verify == "P1 is the winner":
        return jsonify(move=game.board, invalid=True, winner=game.game_result)
    if verify == "draw":
        return jsonify(move=game.board, invalid=True, reason="Draw!", winner="")
    if verify == "This is not your turn, please wait. p1":
        return jsonify(
            move=game.board, invalid=True, reason="This is not your turn.", winner=""
        )
    if verify == "invalid, the col is filled":
        return jsonify(move=game.board, invalid=True, reason="Invalid move, it's filled", winner="")
    if verify == "p1 choose color first please!":
        return jsonify(
            move=game.board, invalid=True, reason="p1 did not choose color", winner=""
        )
    if verify == "p2 choose color first please!":
        return jsonify(
            move=game.board, invalid=True, reason="p2 did not choose color", winner=""
        )
    if verify == "valid":
        game.move(game.player1, col)
        game.winning_move(game.player1)
        game.ChangeTurn()
        game.DecreaseMoves()

        board = ''

        for row in game.board:
            board += str(row) + '.'
        db_move = (game.current_turn, board, game.game_result, game.player1, game.player2, game.remaining_moves)
        db.add_move(db_move)

        return jsonify(move=game.board, invalid=False, winner=game.game_result)


"""
Same as '/move1' but instead proccess Player 2
"""


@app.route("/move2", methods=["POST"])
def p2_move():
    global game
    col = int(request.get_json()["column"][-1])

    verify = game.verify("p2", col)

    if verify == "P2 is the winner":
        return jsonify(move=game.board, invalid=True, winner=game.game_result)
    if verify == "draw":
        return jsonify(move=game.board, invalid=True, reason="Draw!", winner="")
    if verify == "This is not your turn, please wait. p2":
        return jsonify(
            move=game.board, invalid=True, reason="This is not your turn.", winner=""
        )
    if verify == "invalid":
        return jsonify(move=game.board, invalid=True, reason="Invalid move", winner="")
    if verify == "p1 choose color first please!":
        return jsonify(
            move=game.board, invalid=True, reason="p1 did not choose color", winner=""
        )
    if verify == "p2 choose color first please!":
        return jsonify(
            move=game.board, invalid=True, reason="p2 did not choose color", winner=""
        )
    if verify == "valid":
        game.move(game.player2, col)
        game.winning_move(game.player2)
        game.ChangeTurn()
        game.DecreaseMoves()

        board = ''
        for row in game.board:
            board += str(row) + '.'
        db_move = (game.current_turn, board, game.game_result, game.player1, game.player2, game.remaining_moves)
        db.add_move(db_move)

        return jsonify(move=game.board, invalid=False, winner=game.game_result)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
