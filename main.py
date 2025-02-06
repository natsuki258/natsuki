import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# アプリケーションの設定
app = Flask(__name__)

# 環境変数を使用した設定
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = os.getenv("DEBUG") == "True"

# SQLAlchemy の初期化
db = SQLAlchemy(app)

# モデルの定義
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    store = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.get_json()
    
    # 必須項目の確認
    if not all(key in data for key in ["name", "position", "store", "age", "gender", "hire_date"]):
        return jsonify({"error": "Missing data"}), 400
    
    # 日付の形式を正しく変換
    try:
        hire_date = datetime.strptime(data["hire_date"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    
    # 新しい従業員の作成
    new_employee = Employee(
        name=data["name"],
        position=data["position"],
        store=data["store"],
        age=data["age"],
        gender=data["gender"],
        hire_date=hire_date
    )

    # データベースに追加
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"message": "Employee created successfully"}), 201

@app.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    employee_list = [
        {
            "id": emp.id,
            "name": emp.name,
            "position": emp.position,
            "store": emp.store,
            "age": emp.age,
            "gender": emp.gender,
            "hire_date": emp.hire_date.strftime("%Y-%m-%d")
        }
        for emp in employees
    ]
    return jsonify(employee_list)

@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    employee = Employee.query.get(id)
    
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    
    data = request.get_json()
    
    # 更新するデータがある場合のみ変更
    if "name" in data:
        employee.name = data["name"]
    if "position" in data:
        employee.position = data["position"]
    if "store" in data:
        employee.store = data["store"]
    if "age" in data:
        employee.age = data["age"]
    if "gender" in data:
        employee.gender = data["gender"]
    if "hire_date" in data:
        try:
            employee.hire_date = datetime.strptime(data["hire_date"], "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    
    db.session.commit()
    
    return jsonify({"message": "Employee updated successfully"})

@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    employee = Employee.query.get(id)
    
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    
    db.session.delete(employee)
    db.session.commit()
    
    return jsonify({"message": "Employee deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
