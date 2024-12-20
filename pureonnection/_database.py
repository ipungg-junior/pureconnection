import MySQLdb
import json
import redis

class MySQLDatabase:
    def __init__(self, host='localhost', user='root', password='', database='test_db'):
        # Menggunakan MySQLdb untuk menghubungkan ke database MariaDB/MySQL
        self.connection = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password,
            db=database
        )
        self.cursor = self.connection.cursor()

    def insert_data(self, table, data):
        """Memasukkan data ke database"""
        # Menyusun query SQL untuk memasukkan data ke dalam table
        columns = ", ".join(data.keys())
        values = ", ".join([f"'{v}'" for v in data.values()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.cursor.execute(query)
        self.connection.commit()

    def fetch_data(self, table, condition=None):
        """Mengambil data dari database"""
        query = f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        """Menutup koneksi database"""
        self.cursor.close()
        self.connection.close()



class RedisCache:
    def __init__(self, host='localhost', port=6379):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=0)

    def set_data(self, key, data):
        """Menyimpan data di Redis"""
        self.redis_client.set(key, json.dumps(data))

    def get_data(self, key):
        """Mendapatkan data dari Redis"""
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def delete_data(self, key):
        """Menghapus data dari Redis"""
        self.redis_client.delete(key)
