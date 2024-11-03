# Flaskでアプリをリアルタイム更新する方法
#コードを自動で更新して、サーバーを起動するデバックモードを使うためには… (便利)
# export FLASK_APP=「ファイル名」
# export FLASK_ENV=development
# export FLASK_DEBUG=1
# flask run
# このときにwarningが出ても大丈夫！、 * Running on http://〜〜〜 をクリックして開くと開ける

# 備考
# Flaskで一度だけアプリを起動するコマンド
# export FLASK_APP=「ファイル名」
# flask run
# このときにwarningが出ても大丈夫！、 * Running on http://〜〜〜 をクリックして開くと開ける

from flask import Flask
from flask import render_template

app = Flask(__name__)

bullets = [
    '箇条書き１',
    '箇条書き2',
    '箇条書き3',
    '箇条書き4',
    '箇条書き5',
    '箇条書き6',
    '箇条書き１',
    '箇条書き2',
    '箇条書き3',
    '箇条書き4',
    '箇条書き5',
    '箇条書き6',
]

@app.route('/')
def hello():
    return render_template('hello.html', bullets=bullets)

# @app.route('/japan')
# def hello_japan():
#     return "<p>Hello Japanだねぇ</p>"
# @app.route('/america')
# def hello_america():
#     return "<p>Hello Americaだねぇ</p>"


# @app.route('/world')
# def hello_world():
#     return "<p>Hello Worldだねぇ</p>"


# @app.route("/japan/<city>")
# def japan(city):
#     return f"Hello {city} in Japan!"
