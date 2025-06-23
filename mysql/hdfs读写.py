# 导入hdfs的库
# 导入hdfs的模块中InsecureClient类,用于连接HDFS(不启用kerberos安全认证)
from hdfs import InsecureClient
 
 # 第一步:连接hdfs并返回一个客户端对象
def connect_hdfs(url='http://master:9870/'):
    # 异常捕获
    try:
        # 创建一个客户端对象
        client = InsecureClient(url,user='zjs')
        # 打印连接信息
        print('连接hdfs成功')
        return client
    except Exception as e:
        print('连接失败')
        return None

# 第二步hdfs的写操作,将本地文件上传到hdfs。
def write_file_to_hdfs(hdfs_path,local_path,client,overwrite=True):
    
    """"
    将本地文件上传到hdfs
    :param local_path: 本地文件路径
    :param hdfs_path: hdfs文件路径
    :param client: 
    :return: bool值,成功返回True,失败返回False
    """
    try:
        
        client.upload(hdfs_path,local_path,overwrite=overwrite)
        print("上传成功!")
        return True
    except Exception as e:
        print(local_path)
        print(hdfs_path)
        print(e)
        print('上传文件失败!')
        return False
    
# 第四步：hdfs的读操作,将hdfs中的文件下载到本地
def read_file_from_hdfs(hdfs_path,client):
    pass
    """
    从hdfs读取文件的内容
    :param hdfs_path: hdfs上的文件路径
    :param client: 客户端对象
    :return:
    """
    try:
        with client.read(hdfs_path,encoding='utf-8') as reader:
            # 读取内容
            content = reader.read()
            print('文件读取成功!')
            return content
    except Exception as e:
        print('文件读取失败!')
        return None



# 第三步：主函数,连接hdfs的，进行数据写入
def main():
    client = connect_hdfs()
    local_path = "D:\\trian\\train\\jichu\\bill.txt"
    hdfs_path = '/bill.txt'
    # 将数据写入hdfs中
    write_file_to_hdfs(hdfs_path,local_path,client)
    content = read_file_from_hdfs(hdfs_path,client)
    if content:
        print('文件内容: ')
        print(content)

if __name__ == '__main__':
    main()