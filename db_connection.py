import psycopg2

def get_sync_db_connection():
    connection = psycopg2.connect(
        dbname='labsk',
        user='postgres',
        password='12345',
        host='127.0.0.1',
        port='5433'
    )
    print('База данных Postgres успешно подключена!')
    
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f'Версия Postgres: {version[0]}')
    return connection

# Для тестирования подключения
if __name__ == "__main__":
    conn = get_sync_db_connection()
    conn.close()