from pymilvus import MilvusClient


# 简单查询
def query_operation(client: MilvusClient):
    # 1.单向量查询
    res = client.search(
        collection_name="demo_v2",
        data=[
            [
                0.19886812562848388,
                0.06023560599112088,
                0.6976963061752597,
                0.2614474506242501,
                0.838729485096104,
            ]
        ],
        limit=2,
        search_params={"metric_type": "COSINE"},  # 要根据自己创建的索引类型进行填写
        output_fields=["id", "vector"],
    )
    print(res)

    # 2.多向量查询
    res = client.search(
        collection_name="demo_v2",
        data=[
            [
                0.19886812562848388,
                0.06023560599112088,
                0.6976963061752597,
                0.2614474506242501,
                0.838729485096104,
            ],
            [
                0.3172005263489739,
                0.9719044792798428,
                -0.36981146090600725,
                -0.4860894583077995,
                0.95791889146345,
            ],
        ],
        limit=2,
        search_params={"metric_type": "COSINE"},
        output_fields=["id", "vector"],
    )
    print(res)

    # 3.过滤查询
    res = client.search(
        collection_name="demo_v2",
        data=[
            [
                0.19886812562848388,
                0.06023560599112088,
                0.6976963061752597,
                0.2614474506242501,
                0.838729485096104,
            ]
        ],
        limit=5,
        search_params={"metric_type": "COSINE"},
        output_fields=["color"],
        filter="color like 'red%'",
    )
    print(res)

    # 4.范围查询
    # 定义搜索条件
    # 范围搜索: radius：定义搜索空间的外边界。只有距查询向量在此距离内的向量才被视为潜在匹配。
    # range_filter：虽然radius设置搜索的外部限制，但可以选择使用range_filter来定义内部边界，创建一个距离范围，在该范围内向量必须落下才被视为匹配。
    search_params = {
        "metric_type": "COSINE",
        "params": {
            "radius": 0.8,  # 半径范围
            "range_filter": 1,  # 范围过滤器，限制最大不能超过1
        },
    }
    res = client.search(
        collection_name="demo_v2",
        data=[
            [
                0.19886812562848388,
                0.06023560599112088,
                0.6976963061752597,
                0.2614474506242501,
                0.838729485096104,
            ]
        ],
        limit=5,
        search_params=search_params,
        output_fields=["color"],
    )
    print(res)


# 主函数
if __name__ == "__main__":
    # 连接本地Milvus
    client = MilvusClient(uri="http://192.168.100.128:19530")
    # 使用数据库milvus_demo
    client.use_database(db_name="milvus_demo")
    # 查询数据
    query_operation(client)
