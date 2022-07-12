import sqlite3


class User():
    def __init__(self, *args):
        self.id = args[0]
        self.name = args[1]
        self.password = args[2]
        self.is_employee = bool(args[3])
    def __str__(self):
        return f'{self.name}: id={self.id}, is_employee={self.is_employee}'


class DB():

    def __init__(self, db_name):
        self._db_name = db_name
        conn = self._conn()
        conn.execute('''CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            is_employee BOOLEAN)''')
        conn.commit()

    def _conn(self):
        return sqlite3.connect(self._db_name)

    def add_user(self, login, password):
        is_employee = False
        conn = self._conn()
        cur = conn.execute('''INSERT INTO user(name, password, is_employee) 
            VALUES(?, ?, ?)''', (login, password, is_employee))
        conn.commit()
        return User(cur.lastrowid, login, password, is_employee)

    def get_user_by_login(self, login):
        conn = self._conn()
        cur = conn.execute('SELECT id, password, is_employee FROM user WHERE name = ?', (login,))
        data = cur.fetchone()
        if data is None:
            return None
        return User(data[0], login, data[1], data[2])

    def get_user_by_id(self, user_id):
        conn = self._conn()
        cur = conn.execute('SELECT name, password, is_employee FROM user WHERE id = ?', (user_id,))
        data = cur.fetchone()
        if data is None:
            return None
        return User(user_id, data[0], data[1], data[2])

