import sqlite3

DATABASE = "todo.db"


# DBへの接続を開始する関数
def connect_db():
    con=sqlite3.connect(DATABASE)

    # 外部キー制約を有効化
    con.execute("PRAGMA foreign_keys = ON;")
    
    return con


# todoテーブル、usersテーブルを作成する関数
def create_tables():
    con = connect_db()

    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id TEXT UNIQUE,
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


# すべてのToDoの読み込み
def get_todos(u_id):
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM todo WHERE user_id=?", (u_id,))
    todos = cur.fetchall()
    cur.close()
    con.close()
    return todos


# ToDoの追加
def add_todo(t_id, todo, u_id):
    con = connect_db()
    cur = con.cursor()
    cur.execute("INSERT INTO todo (todo_id, todo, is_done, user_id) VALUES (?, ?, 0, ?)", (t_id, todo, u_id))
    con.commit()
    cur.close()
    con.close()


# ToDoの更新
def update_todo(id):
    con = connect_db()
    cur = con.cursor()
    cur.execute("UPDATE todo SET is_done=1 WHERE todo_id=?", (id,))
    con.commit()
    cur.close()
    con.close()


# ToDoの削除
def delete_todo(id):
    con = connect_db()
    cur = con.cursor()
    cur.execute("DELETE FROM todo WHERE todo_id=?", (id,))
    con.commit()
    cur.close()
    con.close()


# ユーザーの追加
def add_user(id, name, password):
    con = connect_db()
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
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_name=?", (name,))
    user = cur.fetchall()
    cur.close()
    con.close()
    return user


# ユーザーIDでのユーザーの読み込み
def get_user_by_id(id):
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (id,))
    user = cur.fetchall()
    cur.close()
    con.close()
    return user
