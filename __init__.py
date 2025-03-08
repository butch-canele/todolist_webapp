from flask import Flask
from .db import create_tables

# 初期化処理
def init_app():
    app = Flask(__name__)
    create_tables()
    return app
