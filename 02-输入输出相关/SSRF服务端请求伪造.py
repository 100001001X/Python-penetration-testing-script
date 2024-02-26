"""
test_ssrf 函数接收目标URL和测试payload，构造URL并发送GET请求。
在示例中，测试payload为 http://malicious-website.com，可以根据具体情况修改成自己的payload。
如果响应中包含"SSRF Vulnerability Test"字符串，则认为存在SSRF漏洞。
请注意，此脚本仅为漏洞检测工具的示例，实际使用时需要谨慎，并确保在授权范围内进行测试。
使用时，替换 target_url 和 ssrf_test_payload 为目标URL和测试payload。
"""
import requests

def test_ssrf(url, test_payload):
    try:
        # 构造带有测试payload的URL
        test_url = url + test_payload
        # 发送HTTP GET请求
        response = requests.get(test_url)
        
        # 输出响应状态码和内容
        print(f"URL: {test_url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Content:\n{response.text}\n")
        
        # 判断是否存在SSRF漏洞
        if "SSRF Vulnerability Test" in response.text:
            print("Vulnerable to SSRF!")
        else:
            print("Not Vulnerable to SSRF.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # 示例使用，替换为目标URL和测试payload
    target_url = "http://example.com/path/"
    ssrf_test_payload = "http://malicious-website.com"

    # 调用测试函数
    test_ssrf(target_url, ssrf_test_payload)
