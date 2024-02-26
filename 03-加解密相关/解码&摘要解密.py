import base64
import hashlib
import urllib.parse

def detect_encryption(ciphertext):
    # 尝试使用Base64解码
    try:
        decoded_text = base64.b64decode(ciphertext)
        print("解码使用Base64:", decoded_text.decode('utf-8'))
        return
    except:
        pass

    # 尝试使用URL解码
    try:
        decoded_text = urllib.parse.unquote(ciphertext)
        print("解码使用URL解码:", decoded_text)
        return
    except:
        pass

    # 尝试使用Unicode解码
    try:
        decoded_text = bytes.fromhex(ciphertext).decode('utf-8')
        print("解码使用Unicode解码:", decoded_text)
        return
    except:
        pass

    # 尝试使用MD5、SHA-1、SHA-256、SHA-3等哈希算法
    hash_algorithms = ['md5', 'sha1', 'sha256', 'sha3_256', 'sha512']
    for algorithm in hash_algorithms:
        try:
            hashed_text = hashlib.new(algorithm, ciphertext.encode()).hexdigest()
            print(f"使用{algorithm.upper()}哈希算法加密: {hashed_text}")
            return
        except:
            pass

    print("无法检测加密方式.")

if __name__ == '__main__':
    ciphertext = input("请输入密文: ")
    detect_encryption(ciphertext)
