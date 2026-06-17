from cryptography.fernet import Fernet
import os

"""
input_file：要加密的原始文件的路径（例如 .env 或任何文件）。
output_file：加密后输出文件的路径（通常命名为 .enc）。
key_file：保存加密密钥的文件的路径。
"""

def encrypt_env_file(input_file, output_file, key_file):
    """加密 .env 文件"""
    with open(input_file, 'rb') as f:
        data = f.read()

        """
with open(...) as f：以二进制读取模式 ('rb') 打开原始文件。
f.read()：读取文件的所有内容，存入变量 data 中（类型为 bytes 字节串）。
with 语句会在代码块结束后自动关闭文件，即使发生异常也会正确关闭，这是一种安全的文件操作方式。
        """

    # 生成 Fernet 密钥
    key = Fernet.generate_key()      #生成一个随机的 32 字节 URL 安全的 Base64 编码密钥，这是 Fernet 加密所要求的格式。每次调用都会生成一个全新的密钥
    with open(key_file, 'wb') as f:
        f.write(key)
    print(f'密钥已保存至: {key_file}')
    """
    以二进制写入模式 ('wb') 打开密钥文件，将生成的密钥写入该文件。
    密钥文件通常保存为 .key 或 .secret，内容是一行字符串。
    打印提示信息，告知用户密钥已保存的位置
    """


    # 加密并保存
    fernet = Fernet(key)    #使用刚才生成的密钥创建一个 Fernet 实例。
    encrypted = fernet.encrypt(data)
    with open(output_file, 'wb') as f:
        f.write(encrypted)
    print(f'加密文件已保存至: {output_file}')
    print(' 请删除原始 .env 文件！')


"""
enc_file：加密文件路径（例如之前生成的 .enc 文件）。
key_file：保存密钥的文件路径。
output_file：解密后输出的文件路径，默认值为 '.env.tmp'（临时文件，防止误覆盖原始文件）。
"""
def decrypt_env_file(enc_file, key_file, output_file='.env.tmp'):
    """解密 .env.enc 文件"""
    # 1. 读取密钥文件
    with open(key_file, 'rb') as f:
        key = f.read()

    # 2. 读取加密文件内容
    with open(enc_file, 'rb') as f:
        encrypted = f.read()

    # 3. 创建 Fernet 解密器并解密
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)   # 如果密钥错误或数据损坏会抛出异常

    # 4. 保存解密后的内容到输出文件（默认 .env.tmp）
    with open(output_file, 'wb') as f:
        f.write(decrypted)

    print(f'解密成功！文件已保存至: {output_file}')

if __name__ == "__main__":
    #     encrypt_env_file(
    #     input_file=r'D:\haha-main\人工智能\.env',
    #     output_file=r'D:\haha-main\人工智能\3.py.enc',
    #     key_file=r'D:\haha-main\人工智能\secret.key'
    # )
    # 加密完成后，手动删除原始 3.py（或者用 os.remove）
        os.remove(r'D:\haha-main\人工智能\.env')

        decrypt_env_file(
        enc_file=r'D:\haha-main\人工智能\3.py.enc',
        key_file=r'D:\haha-main\人工智能\secret.key',
        output_file=r'D:\haha-main\人工智能\.env'
        )