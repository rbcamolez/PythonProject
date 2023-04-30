import os
import mariadb


def relative_path():
    return os.path.dirname(__file__)

# função auxiliar para obter o horário atual


def get_current_time():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_db_conn():
    try:
        # conectando ao banco de dados
        return mariadb.connect(
            user="produtos",
            password="produtos123",
            host="127.0.0.1",
            port=3306,
            database="produtos"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return "Erro ao conectar ao banco de dados."
