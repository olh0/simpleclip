import psycopg2, datetime
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# https://pypi.org/project/db/
#import db.extras  # 如果使用 RealDictCursor 等
# 数据库连接配置
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres.xenfqjnpnjctnrjxxiis",
    "password": "ZcYbvf4eXc5gIMso",
    "host": "aws-0-ap-northeast-1.pooler.supabase.com",
    "port": 6543,
}

db = psycopg2

def get_connection():
    try:
        conn = db.connect(**DB_CONFIG)
        return conn
    except db.Error as e:
        logging.info(f"连接数据库失败: {e}")
        return None  # 或者 raise

def query_execute(query, params=None, fetch=False):
    conn = get_connection()
    if conn == None:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ()) # or () 乃安全措施
            if fetch:
                return cursor.fetchall()
            else:
                conn.commit()
                return True
    except db.Error as e:
        logging.info(f"数据库操作失败：{e}")
        conn.rollback() 
        return False
    finally:
        conn.close()

def init_sql(): 
    query = '''
        CREATE TABLE IF NOT EXISTS clip_contents(
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            text TEXT,
            time TIMESTAMPTZ
            )
        '''
    # query = "select version()"
    return query_execute(query)

def create_contents(text, time):
    
    query = "INSERT INTO clip_contents (text, time) VALUES (%s, %s::timestamptz(0))"
    params = (text, time)
    return query_execute(query, params)

def get_contents():
    query = "SELECT text, time::text FROM clip_contents"
    return query_execute(query, fetch=True)

def delete_contents():
    query = "TRUNCATE TABLE clip_contents RESTART IDENTITY CASCADE"
    return query_execute(query)


# if __name__ == "__main__":

#     # time_iso = "2025-07-01T06:44:17.134Z"
#     time_iso = datetime.datetime.now().isoformat()

#     init_sql()

    # # delete_contents()
    # create_contents("test", time_iso)
    # get_contents()

