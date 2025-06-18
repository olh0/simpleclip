from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话安全

clip_list = ['这是一个简单的网络剪贴板']*5
# clip_list = ['1','2','3','4','5','6']

@app.route('/', methods=['GET'])
def index():
    items = clip_list[::-1][0:6]
    return render_template('index.html', items=items)

@app.route('/add-item', methods=['POST'])
def add_item():
    new_item = request.form.get('new_item')

    if new_item and new_item.strip() != '':
        clip_list.append(new_item)
        updated_items = clip_list[::-1][0:6]

        # 返回JSON响应
        return jsonify({
            'status': 'success',
            'message': '已添加！',
            'items': updated_items
        })
    else:
        return jsonify({
            'status': 'error',
            'message': '请输入有效的内容'
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
