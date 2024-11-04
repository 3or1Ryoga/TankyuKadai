print("hello")
print("world")

from flask import Flask, render_template, request, session, redirect, url_for
import openai

app = Flask(__name__)

# 初期質問とジャンル定義
initial_questions = {
    "環境問題に興味がありますか？": "環境",
    "人権問題に関心がありますか？": "人権",
    "教育格差についてどう思いますか？": "教育"
}

# 各回答のスコア
score_map = {
    "とても興味がある": 5,
    "興味がある": 4,
    "なんとも言えない": 3,
    "あまり興味がない": 2,
    "興味がない": 1
}

@app.route('/recomend2_top')
def index():
    session['scores'] = {genre: 0 for genre in set(initial_questions.values())}
    session['questions_asked'] = list(initial_questions.keys())
    session['additional_question_count'] = 0  # 追加質問のカウント
    return render_template('recomend2_top.html', questions=initial_questions.keys())

@app.route('/submit', methods=['POST'])
def submit():
    # 回答を集計
    for question, genre in initial_questions.items():
        answer = request.form.get(question)
        # session['scores'][genre] += score_map[answer]
        # answerがNoneでないことを確認
        if answer is not None and answer in score_map:
            session['scores'][genre] += score_map[answer]
        else:
            # 不正な回答があった場合の処理
            print(f"無効な回答: {answer} for question: {question}")

    # 途中経過から興味の高いジャンルを特定
    top_interest = max(session['scores'], key=session['scores'].get)
    
    # OpenAI APIを用いて追加質問を生成
    # additional_question = generate_additional_question(top_interest)
    # if additional_question:
    #     session['questions_asked'].append(additional_question)
    #     return render_template('recomend2_additionalQ.html', question=additional_question)
    # else:
    #     return redirect(url_for('result'))
    # 追加質問の回数を確認
    if session['additional_question_count'] < 3:  # 3回まで追加質問を許可
        additional_question = generate_additional_question(top_interest)
        if additional_question:
            session['questions_asked'].append(additional_question)
            session['additional_question_count'] += 1  # カウントを増やす
            return render_template('recomend2_additionalQ.html', question=additional_question)
    
    # 追加質問が終わったら結果に移動
    return redirect(url_for('result'))

def generate_additional_question(genre):
    prompt = f"ユーザーが{genre}に興味があることが分かりました。さらに深い質問を1つ生成してください。"
    
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=50,
    #     temperature=0.7
    # )
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # または "gpt-4"
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        temperature=0.7
    )
    
    # additional_question = response.choices[0].text.strip()
    # return additional_question if additional_question else None
    additional_question = response['choices'][0]['message']['content'].strip()
    return additional_question

@app.route('/result')
def result():
    top_interest = max(session['scores'], key=session['scores'].get)
    return render_template('recomend2_result.html', top_interest=top_interest)

if __name__ == '__main__':
    app.run(debug=True)