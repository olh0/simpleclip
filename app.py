from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话安全

# 数据库初始化函数
def init_db():
    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# 初始化数据库
init_db()

def read_db():
    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    rows = cursor.execute("SELECT id, text, time FROM contents ORDER BY id DESC LIMIT 5").fetchall()
    # 返回最新5条记录（最新在第一位）
    items = [row[1] for row in rows]
    cursor.close()
    conn.close()
    return items

def write_db(add_text):
    conn = sqlite3.connect('clipboard.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contents(text) VALUES (?)", (add_text.strip(),))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/', methods=['GET'])
def index():
    items = read_db()
    return render_template('index.html', items=items)

@app.route('/add-item', methods=['POST'])
def add_item():
    new_item = request.form.get('new_item')
    
    if new_item and new_item.strip() != '':
        # 将新项目写入数据库
        write_db(new_item)
        
        # 读取更新后的列表
        updated_items = read_db()
        
        # 返回JSON响应
        return jsonify({
            'status': 'success',
            'message': '项目已添加！',
            'items': updated_items
        })
    else:
        return jsonify({
            'status': 'error',
            'message': '请输入有效的项目内容'
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
