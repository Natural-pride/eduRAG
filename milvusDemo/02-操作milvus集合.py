#添加索引
from pymilvus import MilvusClient, DataType

def operate_collection(client:MilvusClient):
    # 定义schema
    ## 注意：在定义集合 Schema 时，enable_dynamic_field=True 使得您可以插入未定义的字段。一般动态字段以 JSON 格式存储，通常命名为 $meta。在插入数据时，所有未定义的字段及其值将被保存为键值对。
    ## 在定义集合 Schema 时，auto_id=True 可以对主键自动增长id。
    schema = client.create_schema(auto_id=False, enable_dynamic_field=True) # enable_dynamic_field=True开启动态字段
    # # schema添加字段id, vector
    schema.add_field(field_name='id', datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name='vector', datatype=DataType.FLOAT_VECTOR, dim=5)
    schema.add_field(field_name='scalar', datatype=DataType.VARCHAR, max_length=256, description='标量字段')

    client.create_collection(collection_name="demo_v1",schema=schema)


def add_index(client:MilvusClient):
    # 创建索引参数
    index_params = client.prepare_index_params()
    # # 在向量字段vector上面添加一个索引；
    # index_type='',  # 留空以使用自动索引
    # 对于向量字段，常见的默认索引类型包括IVF_FLAT或HNSW等，具体取决于数据的特性和查询需求。
    # 对于标量字段，常见的默认索引可能是INVERTED等。
    index_params.add_index(field_name="vector", index_type="",metric_type="COSINE",index_name="vector_index")
    # 创建索引
    client.create_index(collection_name="demo_v1", index_params=index_params)
    print("索引创建成功")
    # 查询索引
    indexes = client.list_indexes(collection_name="demo_v1")
    print(f'索引列表：{indexes}')
    # 查询索引详细信息
    res = client.describe_index(collection_name="demo_v1", index_name="vector_index")
    print(f'索引详细信息：{res}')

    #查询索引状态
    print(client.get_load_state(collection_name="demo_v1"))
    # 加载集合
    client.load_collection(collection_name="demo_v1")
    # 查询索引状态
    print(client.get_load_state(collection_name="demo_v1"))


    # 释放集合
    client.release_collection(collection_name="demo_v1")
    # 删除索引
    client.drop_index(collection_name="demo_v1", index_name="vector_index")

    # 标量字段创建索引
    index_params1 = client.prepare_index_params()
    index_params1.add_index(field_name="scalar", index_type="",index_name="scalar_index")
    client.create_index(collection_name="demo_v1", index_params=index_params1)

    # 查询索引
    indexes = client.list_indexes(collection_name="demo_v1")
    print(f'索引列表：{indexes}')
    # 查询索引详细信息
    res = client.describe_index(collection_name="demo_v1", index_name="scalar_index")
    print(f'索引详细信息：{res}')

#主函数
if __name__ == '__main__':
    # 连接本地Milvus
    client = MilvusClient(uri="http://192.168.100.128:19530")
    # 使用数据库milvus_demo
    client.use_database(db_name="milvus_demo")
    # 先执行集合操作
    operate_collection(client)
    # 再执行索引操作
    add_index(client)