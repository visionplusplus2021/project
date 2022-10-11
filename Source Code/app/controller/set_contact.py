import pymongo
from core.database import Database as db
from bson import  json_util,ObjectId
import json

class Set_contact:

    def __init__(self):

        connect_db = db("test")
        self.db = connect_db.db


    def selectContact(self):
        col = self.db['contact']
        docs = col.find().sort("contact_name")
        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)
        return j_data


    def addContact(self,request):
        details = request.form
        document = { 
            'contact_name': details['username'],
            'email': details['email'],
            'mobile': details['mobile']}
        documents = self.db['contact']
        document_inserted_id = documents.insert_one(document).inserted_id

    def deleteContact(self,id):
        self.db['contact'].remove({"_id": ObjectId(ObjectId(id))})


    def editContact(self,id):
        col = self.db['contact']
        docs = col.find({"_id": ObjectId(ObjectId(id))}).sort("contact_name")
        json_data = json_util.dumps(docs)
        j_data = json.loads(json_data)
        return j_data

    def updateContact(self,request,id):
        details = request.form
        self.db['contact'].update({"_id": ObjectId(ObjectId(id))},{"$set": 
                        {
                            "contact_name": details['username'],
                            "email": details['email'],
                            "mobile": details['mobile']
                            
                        }})
            
