from db_connection import MongoDBConnection
import random
import datetime

DB_USER="ivanmoreno"
URI_PASSWORD="05T1y3khqgTbzIvY"
DB_NAME="fichaje"

mongo_user = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, "ivanmoar")

documents = []

for i in range(500):
    randon_number1 = random.randint(0, 59)
    randon_number2 = random.randint(0, 59)
    
    date = datetime.date.today() - datetime.timedelta(days=i)
    start = datetime.time(8, randon_number1, 0)
    finish = datetime.time(17, randon_number2, 0)
    fecha_datetime = datetime.datetime.combine(date, datetime.datetime.min.time())
    document = {"_id":fecha_datetime, "string_id":fecha_datetime.strftime("%d/%m/%Y%H:%M:%S"), 
                "date": date.strftime("%d/%m/%Y"), "outputs": [{"output":start.strftime("%H:%M"), "reason":"-"}], 
                "inputs": [{"input": finish.strftime("%H:%M")}],"modified": False, "nightShift": False}
    randon_number3 = random.randint(1, 20)
    randon_number4 = random.randint(1, 12)
    randon_number5 = random.randint(1, 12)
    
    if i%randon_number4 == 0:
        document["modified"] = True
    
    if i%randon_number5 == 0:
        document["nightShift"] = True


    documents.append(document)

mongo_user.insert_documents(documents)
