# import db

ROW_COUNT = 6
COLUMN_COUNT = 7


class Gameboard:
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = "p1"
        self.remaining_moves = 42

    def setColorForP1(self, color):
        self.player1 = color

    def setColorForP2(self, color):
        self.player2 = color

    # verifty the validation
    def verify(self, curPlayer, col, row):
        if self.game_result == "p1":
            return "P1 is the winner"
        if self.game_result == "p2":
            return "P2 is the winner"
        if self.game_result == "" and self.remaining_moves == 0:
            return "draw"

        if self.player1 == "":
            return "p1 choose color first please!"
        if self.player2 == "":
            return "p2 choose color please"

        if curPlayer != self.current_turn:
            return "This is not your turn, please wait. " + curPlayer

        # verify if the move is valid
        valid_move = False

        for row in range(6, 0, -1):
            if self.board[row - 1][col - 1] == 0:
                valid_move = True
                break

        if valid_move is False:
            return "invalid, the col is filled"

        return "valid"

    def move(self, curColor, col):
        for row in range(6, 0, -1):
            if self.board[row - 1][col - 1] == 0:
                self.board[row - 1][col - 1] = curColor
                break

    def winning_move(self, color):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if (
                    self.board[r][c] == color
                    and self.board[r][c + 1] == color
                    and self.board[r][c + 2] == color
                    and self.board[r][c + 3] == color
                ):
                    if color == self.player1:
                        self.game_result = "p1"
                        break
                    else:
                        self.game_result = "p2"
                        break

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if (
                    self.board[r][c] == color
                    and self.board[r + 1][c] == color
                    and self.board[r + 2][c] == color
                    and self.board[r + 3][c] == color
                ):
                    if color == self.player1:
                        self.game_result = "p1"
                        break
                    else:
                        self.game_result = "p2"
                        break

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if (
                    self.board[r][c] == color
                    and self.board[r + 1][c + 1] == color
                    and self.board[r + 2][c + 2] == color
                    and self.board[r + 3][c + 3] == color
                ):
                    if color == self.player1:
                        self.game_result = "p1"
                        break
                    else:
                        self.game_result = "p2"
                        break

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if (
                    self.board[r][c] == color
                    and self.board[r - 1][c + 1] == color
                    and self.board[r - 2][c + 2] == color
                    and self.board[r - 3][c + 3] == color
                ):
                    if color == self.player1:
                        self.game_result = "p1"
                        break
                    else:
                        self.game_result = "p2"
                        break

    def DecreaseMoves(self):
        if self.remaining_moves != 0:
            self.remaining_moves -= 1
        else:
            return

    def ChangeTurn(self):
        if self.current_turn == "p1":
            self.current_turn = "p2"
        else:
            self.current_turn = "p1"
