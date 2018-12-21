import getter
import pymysql.cursors

def connect():
    #try:
        user = getter.get_user()
        password = getter.get_password()
        cnx = pymysql.connect(
            user=user,
			password = password,
            host = 'localhost',
            db='DATA'
        )
        return cnx

def executeSQL(sql, connection):
    with connection.cursor() as cursor:
        res = cursor.execute(sql)
        connection.commit()
        if res!=0:
            return list(cursor.fetchall())
        else:
            return 0