import json
import os


"""
demo conf.json
{
  "FLASK_SECRET_KEY": "sales-backend",
  "SERVER_PORT": 5000,
  "MYSQL_HOST": "",
  "MYSQL_PORT": 3306,
  "MYSQL_USER": "root",
  "MYSQL_PASSWORD": "123456"
}
"""

# 获取项目根目录并拼接配置文件路径
CONF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.json')
if os.path.exists(CONF_PATH):
    with open(CONF_PATH, 'r', encoding='utf-8') as file:
        conf = json.load(file)
else:
    conf = {}

class Setting:
    debug = conf.get('DEBUG', False)
    flask_secret_key = conf.get('FLASK_SECRET_KEY', 'sales-backend')
    server_port = conf.get('SERVER_PORT', 5000)
    # MYSQL
    mysql_host = conf.get('MYSQL_HOST', '127.0.0.1')
    mysql_port = conf.get('MYSQL_PORT', 3306)
    mysql_user = conf.get('MYSQL_USER', 'root')
    mysql_password = conf.get('MYSQL_PASSWORD', '123456')
    oss_access_id = conf.get('OSS_ACCESS_ID', '')
    oss_access_secret = conf.get('OSS_ACCESS_SECRET', '')
    # 统计任务时间间隔（天），默认1天
    statistics_interval_days = conf.get('STATISTICS_INTERVAL_DAYS', 1)

settings = Setting()
