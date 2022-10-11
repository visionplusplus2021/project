import psycopg2
from bson import json_util
import decimal

import json
from datetime import datetime, date
from time import time, struct_time, mktime


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)
        if isinstance(o, date):
            return str(o)
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, struct_time):
            return datetime.fromtimestamp(mktime(o))
        # Any other serializer if needed
        return super(CustomJSONEncoder, self).default(o)


class ConnectDatabase:

    
    def __init__(self):
        self.conn = psycopg2.connect(database="oshawa", user="postgres",  
            password="p@ssword", host="127.0.0.1")
      
   
    def connectDatabase(self):
       
        return self.conn.cursor()

    def selectData(self,sql_script):

        cursor = self.conn.cursor()

        print("======+> my cursor "+ str(self.conn))
        cursor.execute(sql_script)
        data = cursor.fetchall()
        json_data = json_util.dumps(data, cls=CustomJSONEncoder)

        return json_data
    
    def selectDataByParam(self,sql_script,data):

        cursor = self.conn.cursor()
        cursor.execute(sql_script,data)
        data = cursor.fetchall()
        json_data = json_util.dumps(data, cls=CustomJSONEncoder)

        return json_data



    def insertData(self,sql_script,data):
        try:
            

            cursor = self.connectDatabase()
            print(sql_script)
            cursor.execute(sql_script,data)
            self.conn.commit()
            cursor.close()  


            result = "success"

        except:
            result = "fail"

        return result

    def callSPParam(self,SP_name,data):
        

        cursor = self.connectDatabase()    
        cursor.execute(SP_name,data)
        #cursor.execute("CALL sp_add_new_area(%s,%s);",("UUID", "Test Sittichai"))
        
        self.conn.commit()
        cursor.close()  


        return "true"

    
    def callSP(self,SP_name):
        

        cursor = self.connectDatabase()    
        cursor.execute(SP_name)
        #cursor.execute("CALL sp_add_new_area(%s,%s);",("UUID", "Test Sittichai"))
        
        self.conn.commit()
        cursor.close()  


        return "true"


    def updateData(self,sql_script,data):
        
            

        cursor = self.connectDatabase()
        print(sql_script)
        cursor.execute(sql_script,data)
        self.conn.commit()
        cursor.close()  
        
        print("===Update")

        result = "success"

        
            

        return result

    
    def deleteDataByID(self,sql_script):
    
            
        cursor = self.connectDatabase()

        cursor.execute(sql_script)
        self.conn.commit()
        cursor.close()  

        result = "success"

        
        return result

    def activateStatusByID(self,sql_script):
    
        cursor = self.connectDatabase()

        cursor.execute(sql_script)
        self.conn.commit()
        cursor.close()  

        result = "success"

        
        return result

    def checkExistingData(self,table_name,where_condition):
    
        cursor = self.conn.cursor()

        sql_query = "Select * from "+table_name+ " where "+where_condition
        
        cursor.execute(sql_query)
        data = cursor.fetchall()
        json_data = json_util.dumps(data, cls=CustomJSONEncoder)
        j_data = json.loads(json_data)

        if(len(j_data) == 0 ):
            return False
        else:
            return True
