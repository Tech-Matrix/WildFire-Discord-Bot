import psycopg2
import sys
set_count_num=3
example_id="63560579770220554"
#connect to the db 
try:
    con = psycopg2.connect(
        host = "localhost",
        database="postgres",
        user = "postgres",
        password="mysecretpassword"
    )

#cursor 
    cur = con.cursor()

except Exception as err:
    cur=None
    print("\npsycopg2 error:",err)
    sys.exit()

if cur != None:
    print("\n connection succesful:",con,"\n")

table_name="offences"
sql_statement="SELECT COUNT(*) FROM  offences WHERE offences.id = {};".format(example_id)\

try:
    #sql_object=sql.SQL(sql_statement).format(sql.Identifier(table_name))
    cur.execute(sql_statement)
#if user id and server already exists, add to num_of_offences
    count=cur.fetchall()

    if(count>0):
        cur.execute("UPDATE offences SET num_of_offences = num_of_offences+1 WHERE id= '263560579770220554'")

except Exception as err:
    print("cursor.execute() ERROR:",err)
    con.rollback()
#if num of offences greater than constant, delete user row and ban
cur.execute("SELECT num_of_offences FROM offences WHERE id = '263560579770220554'")
count_num=cur.fetchall()

if(count_num >= set_count_num):
    print("remove user with id",example_id)
#use asyncpg
#take userid and serverid somehow



#execute query
cur.execute("select id, num_of_offences from offences")

rows = cur.fetchall()

for r in rows:
    print (f"id {r[0]} name {r[1]}")

#commit the transcation 
con.commit()

#close the cursor
cur.close()

#close the connection
con.close()
#create function with try except
#read file for table creation