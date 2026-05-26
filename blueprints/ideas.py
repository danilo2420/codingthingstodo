from flask import Blueprint, make_response, jsonify, request
from database import getIdeasCollection, docsToArray, protected, docToDict
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
        return jsonify(docToDict(collection.find_one({"_id": objectId})))
    except Exception as e:
        return jsonify({"error": f"there was an exception: {e}"}, 500)

@ideas_bp.route("/create", methods=["POST"])
@protected
def createIdea():
    try:
        item = request.json["item"]

        # TODO: add validation of object here

        insert_response = collection.insert_one(item)
        return {"inserted_id": str(insert_response.inserted_id)}, 200
    except Exception as e:
        return {"error": f"There was an error: {e}"}, 500


@ideas_bp.route("/update")
@protected
def updateIdea():
    pass

@ideas_bp.route("/delete/<id>")
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
