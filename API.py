from flask import Flask, jsonify, request
import psycopg2
import configparser

config = configparser.RawConfigParser()

config.read('config.ini')

chost = config['DATABASE']['host']
cport = config['DATABASE']['port']
cdb_name = config['DATABASE']['db_name']
cuser = config['DATABASE']['user']
cpassword = str(config['DATABASE']['password'])

app = Flask(__name__)

# Функция для подключения к базе данных
def get_db_connection():
    conn = psycopg2.connect(
    dbname=cdb_name,
    user=cuser,
    password=cpassword,
    host=chost,
    port=int(cport)
)
    return conn

@app.route('/api/data', methods=['GET'])
def get_data():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    ip_filter = request.args.get('ip')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Начинаем составление SQL-запроса
    query = "SELECT * FROM apache_logs WHERE 1=1"
    params = []

    # Добавляем условия на основе переданных параметров
    if start_date:
        query += " AND date >= %s"  # Изменение даты
        params.append(start_date)

    if end_date:
        query += " AND date <= %s"  # Предполагается, что у вас есть поле "date"
        params.append(end_date)

    if ip_filter:
        query += " AND ip = %s"
        params.append(ip_filter)

    try:
        cursor.execute(query, params)
        records = cursor.fetchall()
        
        # Преобразование данных в JSON
        data = [{"date": row[1], "id": row[0], "ip": row[2]} for row in records]  # Измените на ваши колонки
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)