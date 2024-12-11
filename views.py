import psycopg2
import configparser

config = configparser.RawConfigParser()

config.read('config.ini')

chost = config['DATABASE']['host']
cport = config['DATABASE']['port']
cdb_name = config['DATABASE']['db_name']
cuser = config['DATABASE']['user']
cpassword = config['DATABASE']['password']

def console_interface():
    print("Добро пожаловать в систему просмотра данных.")
    
    while True:
        print("\nВыберите действие:")
        print("1 - Просмотреть данные по дате")
        print("2 - Просмотреть данные по IP адресу")
        print("3 - Просмотреть данные по дате и IP адресу")
        print("4 - Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            start_date = input("Введите дату начала (YYYY-MM-DD): ")
            end_date = input("Введите дату окончания (YYYY-MM-DD): ")
            data = get_filtered_data(start_date, end_date)
            print_data(data)

        elif choice == '2':
            ip_filter = input("Введите IP адрес: ")
            data = get_filtered_data(ip_filter=ip_filter)
            print_data(data)

        elif choice == '3':
            start_date = input("Введите дату начала (YYYY-MM-DD): ")
            end_date = input("Введите дату окончания (YYYY-MM-DD): ")
            ip_filter = input("Введите IP адрес: ")
            data = get_filtered_data(start_date, end_date, ip_filter)
            print_data(data)

        elif choice == '4':
            print("Выход из программы...")
            break

        else:
            print("Некорректный ввод. Пожалуйста, попробуйте еще раз.")

def print_data(data):
    if not data:
        print("Нет записей для отображения.")
        return
    for record in data:
        print(record)


def get_filtered_data(start_date=None, end_date=None, ip_filter=None):
    conn = psycopg2.connect(
    dbname=cdb_name,
    user=cuser,
    password=cpassword,
    host=chost,
    port=int(cport)
)
    cursor = conn.cursor()
    
    query = "SELECT * FROM apache_logs WHERE 1=1"
    params = []

    if start_date and end_date:
        query += " AND date BETWEEN %s AND %s"
        params.extend([start_date, end_date])
    
    if ip_filter:
        query += " AND ip = %s"
        params.append(ip_filter)

    cursor.execute(query, params)
    records = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return records

console_interface()