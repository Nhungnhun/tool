import mysql.connector

def check_key_from_db(key_input):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mh08112001",
            database="tool"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT `key` FROM admin_key WHERE `key` = %s", (key_input,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Lỗi: {err}")
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()