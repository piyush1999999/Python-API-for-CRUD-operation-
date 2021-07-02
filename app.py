#My database name is data
#My collection name is profile


from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request 

app=Flask(__name__)
app.secret_key="secret"
app.config['MONGO_URI'] = "mongodb://localhost:27017/data"
mongo=PyMongo(app)


@app.route('/create',methods=['POST']) #add new user to the database
def create_user():
    _json=request.json
    _name=_json['name']
    _email=_json['email']
    _place=_json['place']
    if _name and _email and _place and request.method=='POST':
        id=mongo.db.profile.insert({'name':_name,'email':_email, 'place':_place})
        resp=jsonify("User created successfully")
        resp.status_code=200
        return resp
    else:
        return not_found()

@app.route('/users') #Show all the data stored in the database 
def users():
    users=mongo.db.profile.find()
    resp=dumps(users)
    return resp

@app.route('/delete/<id>',methods=['DELETE']) #delete data from the database using  id
def delete_user(id):
    mongo.db.profile.delete_one({'_id' :ObjectId(id)})
    resp=jsonify("user deleted successfully")
    resp.status_code=200
    return resp

@app.route('/update/<id>', methods=['PUT']) #update data in the database using the id of the data that we need to update
def update_user(id):
    _id=id
    _json=request.json
    _name=_json['name']
    _email=_json['email']
    _place=_json['place']

    if _name and _email and _place and _id and request.method=='PUT':
        mongo.db.profile.update_one({'_id':ObjectId(_id['$old']) if '$old' in _id else ObjectId(_id)},{'$set':{'name':_name, 'email':_email,'place':_place}})
        resp=jsonify("user updated successfully")
        resp.status_code=200
        return resp
    else:
        return not_found()
@app.errorHandler(404) #it will throw the error 'Not Found'
def not_found(error=None):
    message={
        'status':404,
        'message':'Not Found' + request.url
    }
    resp=jsonify(message)
    resp.status_code=404
    return resp



if __name__ == "__main__":
    app.run(debug=True) # it enables the debug mode

