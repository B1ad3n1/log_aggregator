import psycopg2
import re
from datetime import datetime
import configparser

config = configparser.RawConfigParser()

config.read('config.ini')

chost = config['DATABASE']['host']
cport = config['DATABASE']['port']
cdb_name = config['DATABASE']['db_name']
cuser = config['DATABASE']['user']
cpassword = config['DATABASE']['password']


def connect_db():
    try:
        conn = psycopg2.connect(
    dbname=cdb_name,
    user=cuser,
    password=cpassword,
    host=chost,
    port=int(cport)
)
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def process_log_line(line):
    log_pattern = r'(?P<ip>\S+) - - \[(?P<date>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) (?P<http_version>\S+)" (?P<status_code>\d+) (?P<size>\d+)'
    match = re.match(log_pattern, line)
    if match:
        log_data = match.groupdict()
        log_data['date'] = datetime.strptime(log_data['date'], "%d/%b/%Y:%H:%M:%S %z")
        log_data['size'] = int(log_data['size'])
        return log_data
    return None

def insert_log(conn, log_data):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO apache_logs (ip, date, method, path, http_version, status_code, size) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (log_data['ip'], log_data['date'], log_data['method'], log_data['path'], log_data['http_version'], log_data['status_code'], log_data['size'])
        )
    conn.commit()

def main():
    conn = connect_db()
    if not conn:
        return

    try:
        with open('logs/access.log', 'r') as log_file:  # Замените 'access.log' на путь к вашему лог-файлу
            for line in log_file:
                log_data = process_log_line(line)
                if log_data:
                    insert_log(conn, log_data)
                    print(f"Inserted log: {log_data}")
    except FileNotFoundError:
        print("Файл логов не найден. Пожалуйста, проверьте путь к файлу.")

    conn.close()

if __name__ == '__main__':
    main()