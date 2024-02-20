import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress
import csv
import os
from tqdm import tqdm

class PortScanner:
    def __init__(self, target_file, output_path, scan_mode='simple', max_threads=10):
        # 初始化函数，接收目标文件路径、CSV文件输出路径、扫描模式（默认为简单模式）和最大线程数
        self.target_ips = self._parse_target_file(target_file)
        self.output_path = output_path
        self.scan_mode = scan_mode
        self.max_threads = max_threads

    def _parse_target_file(self, target_file):
        # 解析目标文件，将文件中的IP地址提取出来并返回一个列表
        with open(target_file, 'r') as file:
            lines = file.readlines()
            ips = [str(ipaddress.IPv4Address(ip.strip())) for line in lines for ip in line.split() if ipaddress.IPv4Address(ip.strip())]
        return ips

    def _scan_port(self, ip, port):
        # 扫描单个端口的方法，使用socket连接目标IP和端口，获取服务协议
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((ip, port))
                return ip, port, socket.getservbyport(port)
        except (socket.timeout, ConnectionRefusedError):
            return ip, port, ""

    def _scan_ip(self, ip):
        # 扫描单个IP的方法，遍历指定范围的端口，调用_scan_port方法，获取开放的端口信息
        open_ports = []
        ports_to_scan = range(1, 1025) if self.scan_mode == 'simple' else range(1, 65536)
        
        for port in ports_to_scan:
            result = self._scan_port(ip, port)
            if result[2]:
                open_ports.append(result)

        return open_ports

    def scan_ips(self):
        # 扫描所有IP的方法，使用ThreadPoolExecutor进行多线程扫描
        open_ports = []
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_ip = {executor.submit(self._scan_ip, ip): ip for ip in self.target_ips}
            total_tasks = len(future_to_ip)
            with tqdm(total=total_tasks, desc="正在扫描") as pbar:
                for future in as_completed(future_to_ip):
                    pbar.update(1)
                    open_ports.extend(future.result())

        self._write_to_csv(open_ports)

    def _write_to_csv(self, open_ports):
        # 将扫描结果写入CSV文件
        os.makedirs(self.output_path, exist_ok=True)
        csv_file = os.path.join(self.output_path, 'scanreport.csv')
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['IP 地址', '端口', '服务协议'])
            for result in open_ports:
                writer.writerow([result[0], result[1], result[2]])

        print(f"扫描报告已保存至 {os.path.abspath(csv_file)}")

if __name__ == "__main__":
    # 程序入口，接收用户输入，创建PortScanner实例并调用scan_ips方法
    target_file = input("请输入目标文件路径：")
    output_path = input("请输入 CSV 文件输出路径：")
    scan_mode = input("请输入扫描模式（simple/full）：")

    scanner = PortScanner(target_file, output_path, scan_mode=scan_mode.lower())
    scanner.scan_ips()
