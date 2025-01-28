import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# PostgreSQLデータベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemyオブジェクトの初期化
db = SQLAlchemy(app)

# サンプルモデルの定義（テーブル名を'users'に変更）
class User(db.Model):
    __tablename__ = 'users'  # テーブル名を明示的に'users'と指定
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def index():
    try:
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username} for user in users])
        print("Template path:", app.jinja_loader.get_source(app.jinja_env, 'index.html'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
