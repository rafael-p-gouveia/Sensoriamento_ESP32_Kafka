import pymongo
import sys

def db_exists(client,db_name):
    dblist = client.list_database_names()
    if db_name in dblist:
        print("The database '{0}' exists.".format(db_name))
        return True
    else:
        print("The database '{0}' doesn't exists".format(db_name))
        return False

def col_exists(db,col_name):
    collist = db.list_collection_names()
    if col_name in collist:
        print("The collection '{0}' exists.".format(col_name))
        return True
    else:
        print("The collection '{0}' doesn't exists.".format(col_name))
        return False
        
    
print("Hello, World!")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
try:
    myclient.admin.command('ping')
    print("Connection established")
except:
    sys.exit("Connection failed to be established")

mydb = myclient["SensorData"] #not truly created until it gets a collection

db_exists(myclient,"SensorData")

mycol = mydb["data"] #not truly created until it gets content

if(not col_exists(mydb,"data")):
    print("Inserting dummy data in order to ensure database creation")
    mydict = {"_id": "0000-01-01 00:00:00.000000", "Temp": -255, "Umid": -1}
    mycol.insert_one(mydict)
    
    db_exists(myclient,"SensorData")
    assert col_exists(mydb,"data"), "Database and/or collection failed to be created"

print("All set!")
