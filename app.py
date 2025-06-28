from flask import Flask, render_template, request, jsonify
import logging
import datetime
# https://flask.org.cn/en/stable/

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable

app = Flask(__name__)
app.secret_key = 'jjfjjmldhzbwjzswwntx'  # 用于会话安全

 # 初始数据
time_iso = datetime.datetime.now().isoformat()
texts = ['https://github.com/oulh/simpleclip','这是一个简单的网络剪贴板，由 python flask 驱动',
          '数据上传到服务器，不要轻易添加隐私信息！', '数据不支持持久化，能保存多久取决于运行方式及稳定性']
clip_list = [(text, time_iso) for text in texts[::-1]] # 列表模拟剪贴板数据库

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

# 加载列表
@app.route('/get-items', methods=['GET'])
def get_items():
    page = request.args.get('page', 1, type=int) # 加载第一页
    size = request.args.get('size', 8, type=int) # 每页加载8个列表

    items_all = clip_list[::-1]
    total_items = len(items_all)
    # 切片得到每页数据
    start_index = (page - 1) * size
    end_index = (page - 1) * size + size
    items_deliver = items_all[start_index:end_index]
    logging.info(f'已加载{page}页')
    return jsonify({
        'status': 'success',
        # 'items': clip_list[::-1][0:6]
        'items': items_deliver,
        'total': total_items,
        'page': page,
        'size': size,
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
        'items': []
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
    # app.run(debug=True)
