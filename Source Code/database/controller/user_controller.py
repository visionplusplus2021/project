@app.route('/User/activate/<id>', methods=['POST'])
def user_activate(id):

    col = db['user']
    result = col.find_one({'_id': ObjectId(id)})
    json_data = json_util.dumps(result)
    j_data = json.loads(json_data)
    str_activate = "false"
    try:
        if(j_data['feature_activate']) == "false":
            str_activate = "true"
    except:
        pass
    

    document = {
        'timestamp': datetime.timestamp(datetime.now()),
        'user_activate': str_activate
    }

    if (col.update({'_id': ObjectId(id)}, {"$set": document})):
            return 'success'
    else:
        return 'fail', 422  
