
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
]

@app.route("/japan/<city>")
def hello(city):
    return render_template('hello.html', city=city, bullets=bullets)


# Flaskでアプリを一度だけ起動するコマンド
# export FLASK_APP=「ファイル名」
# flask run
# このときにwarningが出ても大丈夫！、 * Running on http://〜〜〜 をクリックして開くと開ける

#コードを自動で更新して、サーバーを起動するデバックモードを使うためには… (便利)
# export FLASK_APP=「ファイル名」
# export FLASK_ENV=development
# export FLASK_DEBUG=1
# flask run


# WindowsのユーザはSQLite３をインストールすること
# その後新しいターミナルを開いて
# pip install flask_sqlalchemy  を打つ
# これはflaskのORマッパー

# pytzもデフォルトで入っていなかった
# pip install pytz を

#データベースを作成
# lsコマンドを用いて、ORマッパーのクラス文があるファイルが表示されることを確認
# python3もしくはpython とターミナルで打ち、対話モードにする

# from app import db を
# db.create_all()

# もし上の2文が無理なら 
#>>> from app import db, app  # Flaskアプリ（appオブジェクト）をインポート
#>>> with app.app_context():   # アプリケーションコンテキストを設定
#...      db.create_all()
# instanceフォルダとblog.dbができるはず