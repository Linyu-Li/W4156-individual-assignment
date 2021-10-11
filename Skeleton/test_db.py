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
        db.init_db()
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
        db.init_db()
        conn = None

        '''
        try:
            conn = sqlite3.connect('sqlite_db')
            cur = conn.cursor()
            cur.execute("INSERT INTO GAME VALUES ('a', 'b', 'c', 'd', 'e', 1)")
            cur.close()

        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()
            '''
        res = db.getMove()

        
    def test_clear(self):
        db.init_db()
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

    def test_add_move_error(self):
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

    def test_getMove_error(self):
        db.init_db()
        db.clear()
        res = db.getMove()

        self.assertNotEqual(res, '')

    def test_clear_error(self):
        db.clear()
        conn = None
        try:
            conn = sqlite3.connect('sqlite_db')
            cur = conn.cursor()
            self.assertIsNotNone(cur.execute('SELECT * FROM GAME'))
            cur.close()
        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()