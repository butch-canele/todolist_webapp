from flask import request, render_template, redirect, url_for, make_response, flash
import uuid
import hashlib
from .__init__ import init_app
from . import db


app = init_app()


"""
Todoリスト

"""
# Todoリスト画面の表示
@app.route("/")
def show_todos():
    u_id = request.cookies.get("u_id")
    db_user = db.get_user_by_id(u_id)
    # cookie認証
    if not u_id or not db_user:
        error = "ログインしてください"
        return render_template("login.html", error=error)
    
    todos = db.get_todos(u_id)
    return render_template("index.html", todos=todos)


# Todoリストの登録
@app.route("/", methods=["POST"])
def create_todo():
    u_id = request.cookies.get("u_id")
    todo = request.form.get("todo")
    id = str(uuid.uuid4())
    db.add_todo(id, todo, u_id)
    return redirect(url_for("show_todos"))


# Todoリストの更新
@app.route("/update", methods=["POST"])
def update_todo():
    id = request.form.get("todo_id")
    print(id)
    db.update_todo(id)
    return redirect(url_for("show_todos"))


# Todoリストの削除
@app.route("/delete", methods=["POST"])
def delete_todo():
    id = request.form.get("todo_id")
    db.delete_todo(id)
    return redirect(url_for("show_todos"))


"""
ユーザー登録

"""
# 登録画面の表示
@app.route("/signup")
def show_signup():
    return render_template("signup.html")


# ユーザー登録
@app.route("/signup", methods=["POST"])
def signup():
    user_name = request.form.get("name")
    password = request.form.get("password")
    db_user = db.get_user_by_name(user_name)

    # ユーザー名がDBに登録済か確認
    if db_user:
        error = "登録済みのユーザー名です"
        return render_template("signup.html", error=error)

    id = str(uuid.uuid4())
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    db.add_user(id, user_name, hashed_password)

    response = make_response(redirect(url_for("show_todos")))
    response.set_cookie("u_id", value=id, max_age=3600)

    return response


"""
ログイン・ログアウト

"""
# ログイン画面の表示
@app.route("/login")
def show_login():
    return render_template("login.html")


# ログイン処理
@app.route("/login", methods=["POST"])
def login():
    user_name = request.form.get("name")
    password = request.form.get("password")
    db_user = db.get_user_by_name(user_name)
    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    if not db_user or hashed_password != db_user[0][2]:
        error = "ユーザー名かパスワードが違います"
        return render_template("login.html", error=error)

    response = make_response(redirect(url_for("show_todos")))
    response.set_cookie("u_id", value=db_user[0][0], max_age=3600)

    return response


# ログアウト処理
@app.route("/logout", methods=["POST"])
def logout():
    response = make_response(redirect(url_for("show_login")))
    response.delete_cookie("u_id")

    return response