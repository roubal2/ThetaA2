import mysql.connector
from src.config import load_config

def get_connection():
    cfg = load_config()
    db_cfg = cfg["database"]
    conn = mysql.connector.connect(
        host=db_cfg["host"],
        user=db_cfg["user"],
        password=db_cfg["password"],
        database=db_cfg["database"],
        port=db_cfg.getint("port", 3306)
    )
    return conn
