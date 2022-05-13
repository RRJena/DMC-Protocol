
import psycopg2
try:
    eol_table_name=["yra1","yra2","yra3","yra_fork3_12"]
    connection = psycopg2.connect(user="postgres",password="koki@123",host="127.0.0.1",port="5432",database="EOL")
    cursor = connection.cursor()
    for eol in eol_table_name:
        sql_update_query = "UPDATE "+eol+" SET production_timestamp=concat(production_date,' ',eol_check_time)::timestamp WHERE production_timestamp is null"
        #sql_update_query = "UPDATE "+eol+" SET production_timestamp=null"
        print(sql_update_query)
        result = cursor.execute(sql_update_query)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into mobile table")
except (Exception, psycopg2.Error) as error:
    print("Failed inserting record into mobile table {}".format(error))
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
                       
