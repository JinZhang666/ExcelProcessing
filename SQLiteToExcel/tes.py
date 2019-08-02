import cx_Oracle
conn = cx_Oracle.connect('appuser', 'appuser', '10.189.66.69:1521/orcl')
cursor = conn.cursor()
cursor.execute('select * from T_TEST ')
result = cursor.fetchall()
print (cursor.rowcount)
for row in result:
    print(row)