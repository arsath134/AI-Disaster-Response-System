from flask import Blueprint
from flask import request
from flask import jsonify

incident_bp = Blueprint("incident", __name__)

@incident_bp.route("/report", methods=["POST"])

def report_incident():

    return jsonify({

        "message":"Incident API working"

    })
