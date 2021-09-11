import psycopg2
import sys
import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        host = "localhost",
        database="postgres",
        user = "postgres",
        password="mysecretpassword"
    )
    #example_id="63560579770220554"
    print("\n connection succesful:",conn,"\n")
    f=open("tablecreation.sql","r")
    data = f.read().replace('\n', '')
    await conn.execute(data)
    await conn.close()

async def fetch_from_db(connection, sql_statement):
    row=connection.fetchrow(sql_statement)
    return row
    
  # return whatever connection.fetch(sql_statement) gives
asyncio.get_event_loop().run_until_complete(main())
#connect to the db 
#try:
#    con = psycopg2.connect(
#        host = "localhost",
#        database="postgres",
#        user = "postgres",
#        password="mysecretpassword"
#    )

#cursor 
#    cur = con.cursor()

#except Exception as err:
#    cur=None
#    print("\npsycopg2 error:",err)
#    sys.exit()


   


#create function with try except
#read file for table creation
