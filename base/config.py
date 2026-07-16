# 导入配置解析库
import configparser
import os
# 导入路径操作库
from pathlib import Path

# 加载 .env 文件中的环境变量（若 python-dotenv 已安装）
try:
    from dotenv import load_dotenv
    # 向上查找项目根目录的 .env
    _env_path = Path(__file__).resolve().parent.parent / '.env'
    if _env_path.exists():
        load_dotenv(dotenv_path=_env_path)
except ImportError:
    pass


class Config:
    # 初始化配置：环境变量(.env) 优先，config.ini 作为回退补充
    def __init__(self, config_file=None):
        # 项目根目录
        self.base_dir = Path(__file__).resolve().parent.parent
        # 解析配置文件路径
        config_path = Path(config_file) if config_file else self.base_dir / 'config.ini'
        if not config_path.is_absolute():
            config_path = self.base_dir / config_path
        # 创建配置解析器
        self.config = configparser.ConfigParser()
        # 读取配置文件（仅用作缺省值来源，可被环境变量覆盖）
        if config_path.exists():
            self.config.read(config_path, encoding='utf-8')

        # -----------------------------
        # 通用取值函数：环境变量 > config.ini > 硬编码缺省值
        # -----------------------------
        def _get(section, key, fallback=None, prefix=''):
            """读取顺序: 环境变量(PREFIX_KEY) -> config.ini -> fallback"""
            env_key = f"{prefix}{key}".upper() if prefix else key.upper()
            env_val = os.environ.get(env_key)
            if env_val is not None:
                return env_val
            return self.config.get(section, key, fallback=fallback)

        def _getint(section, key, fallback=0, prefix=''):
            env_key = f"{prefix}{key}".upper() if prefix else key.upper()
            env_val = os.environ.get(env_key)
            if env_val is not None:
                return int(env_val)
            return self.config.getint(section, key, fallback=fallback)

        # MySQL 配置
        self.MYSQL_HOST = _get('mysql', 'host', fallback='localhost')
        self.MYSQL_USER = _get('mysql', 'user', fallback='root')
        self.MYSQL_PASSWORD = _get('mysql', 'password', fallback='1234')
        self.MYSQL_DATABASE = _get('mysql', 'database', fallback='subjects_kg')

        # Redis 配置
        self.REDIS_HOST = _get('redis', 'host', fallback='localhost')
        self.REDIS_PORT = _getint('redis', 'port', fallback=6379)
        self.REDIS_PASSWORD = _get('redis', 'password', fallback='123456')
        self.REDIS_DB = _getint('redis', 'db', fallback=0)

        # Milvus 配置
        self.MILVUS_HOST = _get('milvus', 'host', fallback='localhost')
        self.MILVUS_PORT = _get('milvus', 'port', fallback='19530')
        self.MILVUS_DATABASE_NAME = _get('milvus', 'database_name', fallback='milvus_demo')
        self.MILVUS_COLLECTION_NAME = _get('milvus', 'collection_name', fallback='edurag')

        # LLM 配置
        self.LLM_MODEL = _get('llm', 'model', fallback='qwen-plus')
        self.DASHSCOPE_API_KEY = _get('llm', 'dashscope_api_key', fallback='')
        self.DASHSCOPE_BASE_URL = _get('llm', 'dashscope_base_url',
                                        fallback='https://dashscope.aliyuncs.com/compatible-mode/v1')

        # 检索参数
        self.PARENT_CHUNK_SIZE = _getint('retrieval', 'parent_chunk_size', fallback=1200)
        self.CHILD_CHUNK_SIZE = _getint('retrieval', 'child_chunk_size', fallback=300)
        self.CHUNK_OVERLAP = _getint('retrieval', 'chunk_overlap', fallback=50)
        self.RETRIEVAL_K = _getint('retrieval', 'retrieval_k', fallback=5)
        self.CANDIDATE_M = _getint('retrieval', 'candidate_m', fallback=2)

        # 应用配置
        valid_sources_raw = _get('app', 'valid_sources', fallback='["ai", "java", "test", "ops", "bigdata"]')
        self.VALID_SOURCES = eval(valid_sources_raw) if isinstance(valid_sources_raw, str) else valid_sources_raw
        self.CUSTOMER_SERVICE_PHONE = _get('app', 'customer_service_phone', fallback='12345678')

        # 日志文件路径
        log_file = _get('logger', 'log_file', fallback='logs/app.log')
        log_path = Path(log_file)
        if not log_path.is_absolute():
            log_path = self.base_dir / log_path
        self.LOG_FILE = str(log_path)


if __name__ == '__main__':
    conf = Config()
    print("LLM_MODEL:", conf.LLM_MODEL)
    print("DASHSCOPE_API_KEY:", conf.DASHSCOPE_API_KEY[:8] + "..." if conf.DASHSCOPE_API_KEY else "EMPTY")
    print("MYSQL_PASSWORD:", conf.MYSQL_PASSWORD)
    print("CHILD_CHUNK_SIZE:", conf.CHILD_CHUNK_SIZE)
    print("VALID_SOURCES:", conf.VALID_SOURCES)
