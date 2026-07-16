from pymilvus import MilvusClient

def operate_db():
    # 连接本地Milvus
    client = MilvusClient(uri="http://192.168.100.128:19530")

    #创建名称为milvus_demo的数据库
    databases = client.list_databases()
    # 判断数据库是否存在
    if 'milvus_demo' not in databases:
        client.create_database(db_name="milvus_demo")
    else:
        client.use_database(db_name="milvus_demo")
#主函数
if __name__ == '__main__':
    # 调用函数
    operate_db()