
import pymongo
import certifi

class Database:

    def __init__(self,database_name):

        self.dbMain = 'mongodb+srv://visionplusplus:visionplusplus@cluster0.gppuu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
        self.client = pymongo.MongoClient(self.dbMain,tlsCAFile=certifi.where())
        self.db = self.client[database_name]

        



