from flask import Blueprint, make_response, jsonify, request
from database import getIdeasCollection, docsToArray, protected, docToDict, validateItem
from bson import ObjectId

ideas_bp = Blueprint("ideas", __name__, url_prefix="/ideas")
collection = getIdeasCollection()

@ideas_bp.route("/list")
@protected
def listIdeas():
    if collection is None:
        return make_response({"error": "Collection could not be loaded"}, 500)
    return jsonify(docsToArray(collection.find()))

@ideas_bp.route("/read/<id>")
@protected
def readIdea(id):
    try:
        objectId = ObjectId(id)
        read_response = collection.find_one({"_id": objectId}) 
        if read_response is None:
            return {"error": "not found"}, 404
        return jsonify(docToDict(collection.find_one({"_id": objectId})))
    except Exception as e:
        return jsonify({"error": f"there was an exception: {e}"}, 500)

@ideas_bp.route("/create", methods=["POST"])
@protected
def createIdea():
    try:
        item = request.json
        if not validateItem(item):
            return {"error": "sent object is not valid"}, 400

        insert_response = collection.insert_one(item)
        return {"inserted_id": str(insert_response.inserted_id)}, 200
    except Exception as e:
        return {"error": f"There was an error: {e}"}, 500


@ideas_bp.route("/update/<id>", methods=["POST"])
@protected
def updateIdea(id):
    try:
        objectId = ObjectId(id)
        update_object = request.json
        update_response = collection.update_one({"_id": objectId}, update_object)
        if update_response.modified_count >= 1:
            return {"message": "item modified successfully"}, 200
        else:
            return {"error": "item not found"}, 404
    except Exception as e:
        return {"error": f"There was an exception: {e}"}, 400

@ideas_bp.route("/delete/<id>", methods=["DELETE"])
@protected
def deleteIdea(id):
    try:
        objectId = ObjectId(id)
        delete_response = collection.delete_one({"_id": objectId})

        if delete_response.deleted_count >= 1:
            return {"message": "item deleted successfully"}, 200
        else:
            return {"error": "item not found"}, 404

    except Exception as e:
        return {"error": f"There was an exception: {e}"}, 400
