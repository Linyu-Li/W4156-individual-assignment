import sqlite3
import unittest
import db
from sqlite3 import Error

class Test_Testdb(unittest.TestCase):
    def test_init_db(self):
        db.init_db()
        conn = None
        try:
            conn = sqlite3.connect('sqlite_db')
            cur = conn.cursor()
            res = cur.execute('SELECT * FROM GAME')
            cur.close()
            self.assertNotEqual(res, "")

        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()

    def test_add_move(self):
        move = ('p1', 'test_board', '', 'red', 'yellow', 42)
        db.add_move(move)
        conn = None

        try:
            conn = sqlite3.connect('sqlite_db')
            cur = conn.cursor()
            exc = cur.execute('SELECT * FROM GAME')
            res = None
            for row in exc:
                res = (row[0], row[1], row[2], row[3], row[4], row[5])
            cur.close()
            self.assertEqual(res, ('p1', 'test_board', '', 'red', 'yellow', 42))

        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()

    def test_getMove(self):
        res = db.getMove()
        tup = None
        for row in res:
            tup = (row[0], row[1], row[2], row[3], row[4], row[5])

        self.assertEqual(tup, ('p1', 'test_board', '', 'red', 'yellow', 42))

    def test_clear(self):
        db.clear()
        conn = None
        try:
            conn = sqlite3.connect('sqlite_db')
            cur = conn.cursor()
            self.assertFalse(cur.execute('SELECT * FROM GAME'))
            cur.close()
        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()

