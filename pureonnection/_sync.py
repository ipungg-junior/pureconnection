import time
from .database import RedisCache, MySQLDatabase

class DataSync:
    def __init__(self, redis_host='localhost', redis_port=6379, db_host='localhost', db_user='root', db_password='', db_name='test_db'):
        self.redis_cache = RedisCache(redis_host, redis_port)
        self.mysql_db = MySQLDatabase(db_host, db_user, db_password, db_name)

    def sync_data(self, table):
        """Sinkronisasi data antara Redis dan database"""
        keys = self.redis_cache.redis_client.keys()
        for key in keys:
            data = self.redis_cache.get_data(key)
            if data:
                # Simpan ke MySQL/MariaDB
                self.mysql_db.insert_data(table, data)
                print(f"Data synced: {data}")
    
    def periodic_sync(self, table, interval=60):
        """Melakukan sinkronisasi data secara periodik"""
        while True:
            self.sync_data(table)
            time.sleep(interval)
