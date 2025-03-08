from mysql.connector import connect, Error

def init_db(app):
    # Initialize database tables if needed
    pass

def get_db_connection(config):
    try:
        return connect(**config)
    except Error as err:
        print(f"MySQL error: {err}")
        return None

def execute_insert(config, sql, val):
    mydb = get_db_connection(config)
    if mydb:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            return True
        except Error as err:
            print(f"MySQL error: {err}")
            mydb.rollback()
            return False
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()
    return False

def execute_cud(config, sql, params):
    mydb = get_db_connection(config)
    if mydb:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql, params)
            mydb.commit()
            return True
        except Error as err:
            print(f"MySQL error: {err}")
            mydb.rollback()
            return False
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()
    return False

def execute_query(config, query, val):
    mydb = get_db_connection(config)
    if mydb:
        try:
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute(query, val)
            return mycursor.fetchall()
        except Error as err:
            print(f"Error executing query: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()
    return None