from db_connection import MongoDBConnection
import datetime

DB_USER="ivanmoreno"
URI_PASSWORD="05T1y3khqgTbzIvY"
DB_NAME="fichaje"

mongo_user = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, "ivanmoar")

documents = []

for i in range(500):
    date = datetime.date.today() - datetime.timedelta(days=i)
    start = datetime.time(8, 0, 0)
    finish = datetime.time(17, 0, 0)
    fecha_datetime = datetime.datetime.combine(date, datetime.datetime.min.time())

    documents.append({"_id":fecha_datetime, "string_id":fecha_datetime.strftime("%d/%m/%Y%H:%M:%S"), "date": date.strftime("%d/%m/%Y"), "start": start.strftime("%H:%M"), "finish": finish.strftime("%H:%M")})

mongo_user.insert_documents(documents)
