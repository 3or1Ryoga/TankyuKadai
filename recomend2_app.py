print("hello")
print("world")

from flask import Flask, render_template, request, session, redirect, url_for
import openai
import os
from dotenv import load_dotenv

# import env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
# 環境変数からAPIキーを取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_API_KEY = env.OPENAI_API_KEY
if OPENAI_API_KEY is None:
    raise ValueError("API key not found. Please set OPENAI_API_KEY in the .env file.")

openai.api_key = OPENAI_API_KEY
# 社会課題の枠組み
topics = ["環境", "人権", "教育", "平和"]

@app.route('/recomend2_top')
def index():
    session['chosen_topic'] = None  # ユーザーが選んだトピックを格納
    session['additional_question_count'] = 0  # 追加質問のカウント
    return render_template('recomend2_top.html', topics=topics)

@app.route('/select_topic', methods=['POST'])
def select_topic():
    # ユーザーが選択した課題の枠組を保存
    session['chosen_topic'] = request.form.get('topic')
    return redirect(url_for('ask_additional_question'))

@app.route('/ask_additional_question')
def ask_additional_question():
    # 追加質問の回数を確認
    if session['additional_question_count'] < 3:  # 3回まで追加質問を許可
        topic = session.get('chosen_topic')
        additional_question = generate_additional_question(topic)
        if additional_question:
            session['additional_question_count'] += 1
            return render_template('recomend2_additionalQ.html', question=additional_question)
    
    # 質問が終わったら結果画面へ移動
    return redirect(url_for('result'))

def generate_additional_question(topic):
    prompt = f"ユーザーが{topic}に興味を持っています。YesかNoで答えられる深い質問を1つ生成してください。"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        temperature=0.7
    )
    
    # 質問を取得して返す
    additional_question = response['choices'][0]['message']['content'].strip()
    return additional_question

@app.route('/result')
def result():
    topic = session.get('chosen_topic')
    
    # 最終的な課題を生成
    prompt = f"ユーザーが{topic}に強い興味を示しています。ユーザーが具体的に取り組みたいと思えるような{topic}に関連する課題を文章形式で提示してください。"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    
    final_task = response['choices'][0]['message']['content'].strip()
    return render_template('recomend2_result.html', topic=topic, final_task=final_task)

if __name__ == '__main__':
    app.run(debug=True)
