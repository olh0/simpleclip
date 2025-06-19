from flask import Flask, render_template, request, jsonify
import logging
import datetime

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话安全

# 使用一个全局变量来模拟剪贴板数据库
# clip_list 存储的是 (内容, ISO格式时间字符串) 的元组
clip_list = [
    ('这是一个简单的网络剪贴板', datetime.datetime.now().isoformat()),
    ('https://www.google.com', datetime.datetime.now().isoformat()),
    ('第二条记录\n支持换行哦！', datetime.datetime.now().isoformat())
] * 6 # 增加一些初始数据

@app.route('/', methods=['GET'])
def index():
    # 返回最新的6条记录，这些记录是元组列表
    items = clip_list[::-1][0:6]
    return render_template('index.html', items=items)

@app.route('/add-item', methods=['POST'])
def add_item():
    new_item_content = request.form.get('new_item')
    current_timestamp = request.form.get('timestamp')

    if new_item_content and new_item_content.strip():
        # 后端生成时间戳，并使用ISO格式，方便前端解析
        # current_timestamp = datetime.datetime.now().isoformat()
        new_item_tuple = (new_item_content.strip(), current_timestamp)
        clip_list.append(new_item_tuple)
        logging.info(f"添加了新项目: {new_item_tuple[0]}，时间: {new_item_tuple[1]}")

        # 返回成功状态和更新后的列表
        return jsonify({
            'status': 'success',
            'message': '已添加！',
            'items': clip_list[::-1][0:6] # 确保这里返回的是元组列表
        })
    else:
        # 如果输入无效，返回错误状态
        return jsonify({
            'status': 'error',
            'message': '请输入有效的内容'
        }), 400

# 用于JS初始加载列表。前端暂用Jinja2方式获取列表
"""
@app.route('/get-items', methods=['GET'])
def get_items():
    return jsonify({
        'status': 'success',
        'items': clip_list[::-1][0:6]
    })
"""
@app.route('/clear-all', methods=['POST'])
def clear_all():
    """
    处理清除所有列表项的请求。
    """
    clip_list.clear() # 清空列表
    logging.info("所有项目已被清除。")

    # 返回成功状态和空的列表
    return jsonify({
        'status': 'success',
        'message': '所有项目已清除',
        'items': [] # 清空后返回空列表
    })

if __name__ == '__main__':
    app.run(debug=True)

