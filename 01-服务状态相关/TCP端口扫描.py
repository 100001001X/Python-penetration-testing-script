import os
import time
from optparse import OptionParser
from random import randint
from scapy.all import *

# 定义一个函数Scan，用于扫描指定IP地址的端口
def Scan(ip):
    try:
        dport = random.randint(1, 65535)    # 随机选择目的端口号
        packet = IP(dst=ip)/TCP(flags="A",dport=dport)  # 构造TCP数据包，标志位设置为ACK，目的端口随机选择
        response = sr1(packet, timeout=1.0, verbose=0)  # 发送数据包并等待1秒钟获取响应
        if response:
            if response[TCP].flags == 'R' or response[TCP].flags == 'RA':  # 判断响应包中是否存在RST标志位（重置连接）
                time.sleep(0.5)
                print(ip + ' ' + "is up")  # 如果存在，表示端口是开放的
            else:
                print(ip + ' ' + "is down")  # 否则端口是关闭的
        else:
            print(ip + ' ' + "is down")  # 如果没有响应，表示端口是关闭的
    except:
        pass

# 定义主函数main
def main():
    usage = "Usage: %prog -i <ip address>"  # 输出帮助信息
    parse = OptionParser(usage=usage)
    parse.add_option("-i", '--ip', type="string", dest="targetIP", help="specify the IP address")   # 获取用户输入的目标IP地址
    options, args = parse.parse_args()  # 解析用户输入的参数
    if '-' in options.targetIP:
        # 如果输入的是一个IP地址范围，例如：192.168.1.1-255
        # 将IP地址范围进行分割，并循环遍历所有IP地址
        for i in range(int(options.targetIP.split('-')[0].split('.')[3]), int(options.targetIP.split('-')[1]) + 1):
            Scan(options.targetIP.split('.')[0] + '.' + options.targetIP.split('.')[1] + '.' +
                     options.targetIP.split('.')[2] + '.' + str(i))
    else:
        Scan(options.targetIP)  # 如果输入的是单个IP地址，则直接进行扫描

# 如果该脚本作为独立程序运行，则执行主函数
if __name__ == '__main__':
    main()
