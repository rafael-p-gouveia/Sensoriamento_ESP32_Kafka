import pymongo
import sys

#Print if database with expecified name exist
def db_exists(client,db_name):
    dblist = client.list_database_names()
    if db_name in dblist:
        print("The database '{0}' exists.".format(db_name))
        return True
    else:
        print("The database '{0}' doesn't exists".format(db_name))
        return False

#Print if column with expecified name exist
def col_exists(db,col_name):
    collist = db.list_collection_names()
    if col_name in collist:
        print("The collection '{0}' exists.".format(col_name))
        return True
    else:
        print("The collection '{0}' doesn't exists.".format(col_name))
        return False


#Attemp to connect to MongoDB application
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
try:
    myclient.admin.command('ping')
    print("Connection established")
except:
    sys.exit("Connection failed to be established")

#If succeded, selects the desired database
mydb = myclient["SensorData"] #Not truly created until it gets a collection

#Checks if the database existed or not and print the conclusion
db_exists(myclient,"SensorData")

#Selects the desired column
mycol = mydb["data"] #not truly created until it gets content

#If they do not already exist, insert dummy data
if(not col_exists(mydb,"data")):
    print("Inserting dummy data in order to ensure database creation")
    mydict = {"_id": "0000-01-01 00:00:00.000000", "Temp": -255, "Umid": -1}
    mycol.insert_one(mydict)
    
    #Test if column was successfully created
    db_exists(myclient,"SensorData")
    assert col_exists(mydb,"data"), "Database and/or collection failed to be created"

print("All set!")
