from flask import Flask, render_template, request, jsonify
import logging
import datetime

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable
app = Flask(__name__)
app.secret_key = 'jjfjjmldhzbwjzswwntx'  # 用于会话安全

time_iso = datetime.datetime.now().isoformat()
# 列表模拟剪贴板数据库
# clip_list 存储的是 (内容, ISO格式时间字符串) 的元组
clip_list = [
    ('若非要添加隐私信息，请及时清理！', time_iso),
    ('数据保存在服务器，勿轻易上传隐私信息！', time_iso),
    ('https://www.google.com', time_iso),
    ('这是一个简单的网络剪贴板', time_iso),
] * 8 # 初始数据

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add-item', methods=['POST'])
def add_item():
    new_item_content = request.form.get('new_item')
    current_timestamp = request.form.get('timestamp')

    if new_item_content and new_item_content.strip():
        new_item_tuple = (new_item_content.strip(), current_timestamp)
        clip_list.append(new_item_tuple)
        logging.info(f"添加了新内容: {new_item_tuple[0]}，时间: {new_item_tuple[1]}")

        # 返回成功状态和更新后的列表
        return jsonify({
            'status': 'success',
            'message': '已添加！',
            'items': clip_list[::-1]
            # 'items': clip_list[::-1][0:6] #限制列表数量
        })
    else:
        # 如果输入无效，返回错误状态
        return jsonify({
            'status': 'error',
            'message': '请输入有效的内容'
        }), 400

# 用于JS初始加载列表。

@app.route('/get-items', methods=['GET'])
def get_items():
    # page = request.args.get('page', 1, type=int)
    # size = request.args.get('size', 8, type=int)
    page = 1
    size = 8
    items_all = clip_list[::-1]
    total_items = len(items_all)
    # 0:8
    # 8:16
    # 16:24
    start_index = (page - 1) * size
    end_index = (page - 1) * size + size
    items_deliver = items_all[start_index:end_index]

    return jsonify({
        'status': 'success',
        # 'items': clip_list[::-1][0:6]
        'items': items_deliver,
        'total': total_items,
        'page': page,
        # 'size': size,
    })

@app.route('/clear-all', methods=['POST'])
def clear_all():
    """
    处理清除所有列表项的请求。
    """
    clip_list.clear() # 清空列表
    logging.info("所有内容已被清除。")

    # 返回成功状态和空的列表
    return jsonify({
        'status': 'success',
        'message': '所有内容已清除',
        'items': [] # 清空后返回空列表
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
    # app.run(debug=True)
