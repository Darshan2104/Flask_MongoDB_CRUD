from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.company
    mongo.server_info() # trigger exception if can't connect to db
except:
    print("Error- cannot connect to db")

########################

@app.route("/users", methods= ["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        # print(data)
        return Response(
            response= json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({
                    "message" : "Can't read Users"
                }),
            status=500,
            mimetype="application/json"
        )


########################
@app.route("/users", methods = ["POST"])
def create_user():
    try:
        # user =  {"name":"B", "lastname" :"BB"}

        user =  {"name": request.form['name'], "lastname" :request.form['lastname']}

        # user = {
        #     #in form enter key what you have set in postman!
        #     "name": request.form["name"],   
        #     "lastname": request.form["lastname"]
        # }
        dbResponse = db.users.insert_one(user) # In the database 'company' (db) it will check for 'users' if not there it will create one and insert one
        
        # check all the available options
        # for attr in dir(dbResponse):
        #     print(attr)

        # print(dbResponse.inserted_id)

        return Response(
            response= json.dumps({
                    "message" : "User is created",
                    "id":f"{dbResponse.inserted_id}"
                }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)

########################
@app.route("/users/<id>",methods = ["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
           {"_id":ObjectId(id)},
           {"$set":{"name": request.form["name"]}}
        )

        # if else is for if we do not make any change!!!

        if dbResponse.modified_count == 1:
            return Response(
                response= json.dumps({
                        "message" : "User updated"         
                    }),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response= json.dumps({
                        "message" : "nothing to update"         
                    }),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({
                    "message" : "Sorry, can not update user!"         
                }),
            status=500,
            mimetype="application/json"
        )

########################
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        
        if dbResponse.deleted_count == 1:
            return Response(
                response= json.dumps({
                        "message" : "User deleted",
                        "id": f"{id}"         
                    }),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response= json.dumps({
                        "message" : "User NOt found ",
                    }),
                status=200,
                mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({
                    "message" : "can't delete user"         
                }),
            status=500,
            mimetype="application/json"
        )

########################
if __name__ == "__main__":
    app.run(port=8090, debug=True)