from flask import Blueprint, make_response, jsonify, request
from database import getIdeasCollection, docsToArray, protected

ideas_bp = Blueprint("ideas", __name__, url_prefix="/ideas")

@ideas_bp.route("/list")
@protected
def listIdeas():
    collection = getIdeasCollection()

    if collection is None:
        return make_response({"error": "Collection could not be loaded"}, 500)
    return jsonify(docsToArray(collection.find()))