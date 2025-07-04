from flask import Flask, render_template, request, jsonify
import clip_sql as sql
import logging
import datetime
# https://flask.org.cn/en/stable/

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable

app = Flask(__name__)
app.secret_key = 'jjfjjmldhzbwjzswwntx'  # 用于会话安全


def initial_list(sql_success):
    global clip_list
    time_iso = datetime.datetime.now().isoformat()
    if sql_success:
        clip_list = sql.get_contents()
    else:
        clip_list = [0]
    if clip_list == []:
        texts = ['https://github.com/oulh/simpleclip','这是一个简单的网络剪贴板，由 python flask 驱动',
            '数据上传到服务器，不要轻易添加隐私信息！', '数据不支持持久化，能保存多久取决于运行方式及稳定性']
        for text in texts[::-1]:
            sql.create_contents(text, time_iso)
            logging.info("已初始化一条记录...")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add-item', methods=['POST'])
def add_item():
    new_item_content = request.form.get('new_item')
    current_timestamp = request.form.get('timestamp')
    
    if new_item_content and new_item_content.strip():

        if sql.create_contents(new_item_content.strip(), current_timestamp):
            # 为了提高页面反应速度，使用列表变量拷贝数据
            new_item_tuple = (new_item_content.strip(), current_timestamp)
            clip_list.append(new_item_tuple)       
            logging.info(f"添加了新内容: {new_item_content}，时间: {current_timestamp}")
        # 返回成功状态和更新后的列表
            return jsonify({
                'status': 'success',
                'message': '已添加！',
                'items': clip_list[::-1]
            })
        else:
            return jsonify({
                'status': 'error',
                'message': '数据库错误，添加失败',
                'items': clip_list[::-1]
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
    status = 'sql_error' if clip_list == [0] else 'success'
    
    page = request.args.get('page', 1, type=int) # 加载第一页
    size = request.args.get('size', 8, type=int) # 每页加载8个列表
    # clip_list = sql.get_contents()
    # logging.info(f"database----query:{clip_list}")
    items_all = clip_list[::-1]
    total_items = len(items_all)
    # 切片得到每页数据
    start_index = (page - 1) * size
    end_index = (page - 1) * size + size
    items_deliver = items_all[start_index:end_index]
    logging.info(f'已加载{page}页')
    
    return jsonify({
        'status': status,
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
    if sql.delete_contents():
        logging.info("所有内容已被清除。")   
         # 返回成功状态和空的列表
        return jsonify({
            'status': 'success',
            'message': '所有内容已清除',
            'items': []
        })
    else:
        return jsonify({
            'status': 'error',
            'message': '数据库错误，清除失败',
            'items': clip_list
        })


if __name__ == '__main__':
    sql_success = sql.init_sql()
    logging.info(f"数据库状态：{sql_success}")
    initial_list(sql_success)
    app.run(debug=True, host='0.0.0.0', port='5001')
    # app.run(debug=True)