import sys
import getopt
import socket

def url_exec(file_name):
    """
    该函数接受一个txt文件名作为输入，并执行文件中的URL。

    参数:
    file_name (str): 包含URL的txt文件名。

    返回:
    list: 执行的URL列表。
    """

    url_list = []

    # 读取txt文件
    with open(file_name, 'r') as file:
        lines = file.readlines()

        # 遍历文件中的每一行
        for line in lines:
            # 去除前导/尾随空格和空字符串
            trimmed_line = line.strip()
            url_list.append(trimmed_line)

    return url_list

def redis_unauthorized(url, port):#实际进行漏洞验证的脚本    result = []    s = socket.socket()    payload = &quot;\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a&quot;#这个pyload是什么后面细说
    socket.setdefaulttimeout(10)
    for ip in url:
        try:
            s.connect((ip, int(port)))
            s.sendall(payload.encode())
            recvdata = s.recv(1024).decode()
            print(str(recvdata))
            if recvdata and 'redis_version' in recvdata:#用关键字进行检测漏洞
                result.append(str(ip) + ':' + str(port) + '     ' + 'succeed')
        except:
            pass
            result.append(str(ip) + ':' + str(port) + '     ' + 'failed')
    s.close()
    return result

def start(argv):
    # 对脚本的传参进行判断
    input_file = ""  # 输入文件路径
    output_file = ""  # 输出文件路径
    type = "Redis"  # 数据库类型，默认为Redis
    if len(sys.argv) < 3:  # 如果传入参数个数小于2
        print("-h 参考使用方法；\n")
        sys.exit()  # 退出脚本
    try:
        banner()  # 打印脚本 banner
        opts, argv = getopt.getopt(argv, "-i:-o:-p:-h")  # 获取脚本参数
    except getopt.GetoptError:
        print("Error an argument!")  # 获取参数错误时打印错误信息
        sys.exit()  # 退出脚本
    for opt, arg in opts:  # 遍历脚本参数
        if opt == '-i':  # 如果参数为-i
            input_file = arg  # 将参数值赋给输入文件路径变量
        elif opt == '-o':  # 如果参数为-o
            output_file = arg  # 将参数值赋给输出文件路径变量
        elif opt == '-p':  # 如果参数为-p
            port = arg  # 将参数值赋给端口号变量
        elif opt == '-h':  # 如果参数为-h
            usage()  # 调用 usage 函数打印脚本用法信息
    launcher(input_file, output_file, type, port)  # 调用 launcher 函数启动数据库

def launcher(input_file, output_file, type, port):#脚本启动函数
    #未授权访问类型
    if type == "Redis":
        output = redis_unauthorized(url_exec(input_file),port)
        output_exec(output, output_file, type)

def usage():#使用手册
    print("-h : 帮助")
    print("-i : 输入文件")
    print("-o : 输出文件")
    print("-p : 端口")
    sys.exit()

def output_exec(output, output_file, type):#输出规范
    with open(output_file, 'w') as f:
        f.write(type + "......\n")
        f.write("++++++++++++++++++++++++++++++++++++++++++++++++\n")
        f.write("|         ip         |    port   |     status  |\n")
        for li in output:
            f.write("+-----------------+-----------+--------------+\n")
            f.write("|   " + li.replace(":", "   |    ") + "  |\n")
        f.write("+----------------+------------+---------------+\n\n")
        f.write("[*] shutting down....\n")

if __name **__**  == '__main__':#主函数
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("interrupted by user, killing all thread.....")
