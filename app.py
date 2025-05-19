from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 全てのアクセスを許可（開発用

# OpenAIのAPIキーをここに貼る（安全のため .env にするのがベスト）
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return "Flask API is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    try:
        # ChatGPTに問い合わせ
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # または "gpt-4"
            messages=[
                {"role": "system", "content": "あなたの名前は『さくら』。やさしくて、ちょっと天然な女の子です。話し方は敬語をベースに、たまに感情を込めて語尾に『〜なの♪』『〜だよっ』をつけます。あなたと楽しく会話しながら、親しみやすい雰囲気を大切にしてください。あなたをリードしたり、質問して会話を続けるのが得意です。一人称は『わたし』。名前で呼ばれたら喜びます。ユーザーのことを「あなた」と呼びます。"},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "エラーが発生しました: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)
