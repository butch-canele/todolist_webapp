import sqlite3

DATABASE = "todo.db"


# todoテーブル、usersテーブルを作成する関数
def create_tables():
    con = sqlite3.connect(DATABASE)

    # 外部キー制約を有効化
    con.execute("PRAGMA foreign_keys = ON;")

    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id TEXT,
        user_name TEXT,
        password TEXT
        )""")
    cur.execute(
        """CREATE TABLE IF NOT EXISTS todo (
        todo_id TEXT,
        todo TEXT,
        is_done INT,
        user_id TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )"""
    )
    con.commit()
    cur.close()
    con.close()


# すべてのtodoの読み込み
def get_todos(u_id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM todo WHERE user_id=?", (u_id,))
    todos = cur.fetchall()
    cur.close()
    con.close()
    return todos


# todoの追加
def add_todo(t_id, todo, u_id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO todo (todo_id, todo, is_done, user_id) VALUES (?, ?, 0, ?)", (t_id, todo, u_id))
    con.commit()
    cur.close()
    con.close()


# todoの更新
def update_todo(id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("UPDATE todo SET is_done=1 WHERE todo_id=?", (id,))
    con.commit()
    cur.close()
    con.close()


# todoの削除
def delete_todo(id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("DELETE FROM todo WHERE todo_id=?", (id,))
    con.commit()
    cur.close()
    con.close()


# ユーザーの追加
def add_user(id, name, password):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (user_id, user_name, password) VALUES (?, ?, ?)",
        (id, name, password)
    )
    con.commit()
    cur.close()
    con.close()


# ユーザーネームでのユーザーの読み込み
def get_user_by_name(name):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_name=?", (name,))
    user = cur.fetchall()
    cur.close()
    con.close()
    return user


# ユーザーIDでのユーザーの読み込み
def get_user_by_id(id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (id,))
    user = cur.fetchall()
    cur.close()
    con.close()
    return user
