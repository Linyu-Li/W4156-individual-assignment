from Gameboard import Gameboard
import unittest


gb = None


class Test_TestGameboard(unittest.TestCase):
    def setUp(self):
        global gb
        gb = Gameboard()

    def tearDown(self):
        global gb
        gb = None

    def test_setColorForP1(self):
        # Check set color function
        gb.setColorForP1("red")
        self.assertEqual(gb.player1, "red")

    def test_setColorForP2(self):
        # Check set color function
        gb = Gameboard()
        gb.setColorForP2("yellow")
        self.assertEqual(gb.player2, "yellow")

    def test_DecreaseMoves(self):
        # Check decrease moves function
        gb.DecreaseMoves()
        self.assertEqual(gb.remaining_moves, 41)

    def test_DecreaseMoves_when_0_step(self):
        # Check decrease function when remaining step is 0
        gb.remaining_moves = 0
        gb.DecreaseMoves()
        self.assertEqual(gb.remaining_moves, 0)

    def test_ChangeTurn_for_p1(self):
        # Check change turn function
        gb.current_turn = "p1"
        gb.ChangeTurn()
        self.assertEqual(gb.current_turn, "p2")

    def test_ChangeTurn_for_p2(self):
        # Check change turn function
        gb.current_turn = "p2"
        gb.ChangeTurn()
        self.assertEqual(gb.current_turn, "p1")

    def test_move(self):
        # Check if move function is ok

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        gb.move("red", 1)
        self.assertEqual(gb.board[5][0], "red")

    def test_correct_move(self):
        # Checks if this move is a happy path for correct move
        gb.player1 = "red"
        gb.player2 = "yellow"

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                verify = gb.verify(gb.current_turn, col, row)
                self.assertEqual(verify, "valid")

    def test_not_current_players_turn(self):
        # Checks if it's an invalid move - it is not current player's turn
        gb.player1 = "red"
        gb.player2 = "yellow"

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        # Check if it is not p2's turn
        gb.current_turn = "p1"
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                verify = gb.verify("p2", col, row)
                self.assertEqual(verify, "This is not your turn, please wait. p2")

        # Check if it is not p1's turn
        gb.current_turn = "p2"
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                verify = gb.verify("p1", col, row)
                self.assertEqual(verify, "This is not your turn, please wait. p1")

    def test_winner_already_declared(self):
        # Check if it's an invalid move - winner already declared

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        # Check if p1 is the winner
        gb.game_result = "p1"

        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                verify = gb.verify("p1", col, row)
                self.assertEqual(verify, "P1 is the winner")

        # Check if p2 is the winner
        gb.game_result = "p2"

        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                verify = gb.verify("p2", col, row)
                self.assertEqual(verify, "P2 is the winner")

    def test_draw(self):
        # Check if it's an invalid move - it's a draw
        gb.game_result = ""
        gb.remaining_moves = 0

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                verify = gb.verify(gb.current_turn, col, row)
                self.assertEqual(verify, "draw")

    def test_current_column_is_filled(self):
        # Check if it's an invalid move - currrent column is filled

        gb.player1 = "red"
        gb.player2 = "yellow"

        # Initialize the gameboard, but every col is filled
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 1

        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                verify = gb.verify(gb.current_turn, col, row)
                self.assertEqual(verify, "invalid, the col is filled")

    def test_p1_not_choose_color(self):
        # Check if p1 did not choose the color

        gb.player1 = ""

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                verify = gb.verify(gb.player1, col, row)
                self.assertEqual(verify, "p1 choose color first please!")

    def test_p2_not_choose_color(self):
        # Check if p2 did not choose the color

        gb.player1 = "red"
        gb.player2 = ""

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                verify = gb.verify(gb.player2, col, row)
                self.assertEqual(verify, "p2 choose color please")

    def test_winning_move_horizontal_for_p1(self):
        # Checks if there is a winning move in horizontal direction

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        gb.player1 = "red"
        gb.player2 = "yellow"

        gb.board[5][0] = "red"
        gb.board[5][1] = "red"
        gb.board[5][2] = "red"
        gb.board[5][3] = "red"

        gb.winning_move(gb.player1)
        self.assertEqual(gb.game_result, "p1")

    def test_winning_move_horizontal_for_p2(self):
        # Checks if there is a winning move in horizontal direction

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        gb.player1 = "red"
        gb.player2 = "yellow"

        gb.board[5][0] = "yellow"
        gb.board[5][1] = "yellow"
        gb.board[5][2] = "yellow"
        gb.board[5][3] = "yellow"

        gb.winning_move(gb.player2)
        self.assertEqual(gb.game_result, "p2")

    def test_winning_move_vertical_for_p1(self):
        # Checks if there is a winning move in vertical direction

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        gb.player1 = "red"
        gb.player2 = "yellow"

        gb.board[5][0] = "red"
        gb.board[4][0] = "red"
        gb.board[3][0] = "red"
        gb.board[2][0] = "red"

        gb.winning_move(gb.player1)
        self.assertEqual(gb.game_result, "p1")

    def test_winning_move_vertical_for_p2(self):
        # Checks if there is a winning move in vertical direction

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        gb.player1 = "red"
        gb.player2 = "yellow"

        gb.board[5][0] = "yellow"
        gb.board[4][0] = "yellow"
        gb.board[3][0] = "yellow"
        gb.board[2][0] = "yellow"

        gb.winning_move(gb.player2)
        self.assertEqual(gb.game_result, "p2")

    def test_winning_move_negatively_slope_diaganol_for_p1(self):
        # Checks if there is a winning move in negatively slope diaganol

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        gb.player1 = "red"
        gb.player2 = "yellow"

        gb.board[2][3] = "red"
        gb.board[3][2] = "red"
        gb.board[4][1] = "red"
        gb.board[5][0] = "red"

        gb.winning_move(gb.player1)
        self.assertEqual(gb.game_result, "p1")

    def test_winning_move_negatively_slope_diaganol_for_p2(self):
        # Checks if there is a winning move in negatively slope diaganol

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        gb.player1 = "red"
        gb.player2 = "yellow"

        gb.board[2][3] = "yellow"
        gb.board[3][2] = "yellow"
        gb.board[4][1] = "yellow"
        gb.board[5][0] = "yellow"

        gb.winning_move(gb.player2)
        self.assertEqual(gb.game_result, "p2")

    def test_winning_move_postively_slope_diaganol_for_p1(self):
        # Checks if there is a winning move in positively slope diaganol

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        gb.player1 = "red"
        gb.player2 = "yellow"

        gb.board[0][0] = "red"
        gb.board[1][1] = "red"
        gb.board[2][2] = "red"
        gb.board[3][3] = "red"

        gb.winning_move(gb.player1)
        self.assertEqual(gb.game_result, "p1")

    def test_winning_move_postively_slope_diaganol_for_p2(self):
        # Checks if there is a winning move in positively slope diaganol

        # Initialize the gameboard
        for row in range(6, 0, -1):
            for col in range(7, 0, -1):
                gb.board[row - 1][col - 1] = 0

        gb.player1 = "red"
        gb.player2 = "yellow"

        gb.board[0][0] = "yellow"
        gb.board[1][1] = "yellow"
        gb.board[2][2] = "yellow"
        gb.board[3][3] = "yellow"

        gb.winning_move(gb.player2)
        self.assertEqual(gb.game_result, "p2")
