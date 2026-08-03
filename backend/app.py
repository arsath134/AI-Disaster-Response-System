from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import uuid
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


# -----------------------------
# AWS CONFIGURATION
# -----------------------------

AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")

DYNAMODB_TABLE = os.getenv(
    "DYNAMODB_TABLE",
    "DisasterReports"
)

S3_BUCKET = os.getenv(
    "S3_BUCKET",
    "ai-disaster-response-images"
)


# AWS Clients

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


table = dynamodb.Table(DYNAMODB_TABLE)


# -----------------------------
# HOME API
# -----------------------------

@app.route("/")
def home():

    return jsonify({
        "project": "AI Disaster Response System",
        "status": "Running",
        "version": "1.0"
    })


# -----------------------------
# HEALTH CHECK
# -----------------------------

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "server": "EC2 Flask Backend"
    })


# -----------------------------
# AI DISASTER ANALYSIS
# -----------------------------

def analyze_disaster(disaster, severity):

    """
    Temporary AI logic.
    Later replace with:
    - AWS Bedrock
    - OpenAI API
    - SageMaker Model
    """

    if severity.lower() == "high":

        risk = "Critical"

        recommendation = (
            "Immediate evacuation required. "
            "Alert emergency response teams."
        )

    elif severity.lower() == "medium":

        risk = "Moderate"

        recommendation = (
            "Monitor situation and prepare emergency resources."
        )

    else:

        risk = "Low"

        recommendation = (
            "Continue monitoring disaster updates."
        )


    return {
        "risk": risk,
        "recommendation": recommendation
    }



# -----------------------------
# SUBMIT DISASTER REPORT
# -----------------------------

@app.route("/report", methods=["POST"])
def create_report():

    try:

        data = request.json


        report_id = str(uuid.uuid4())


        location = data.get(
            "location",
            "Unknown"
        )

        disaster = data.get(
            "disaster",
            "Unknown"
        )

        severity = data.get(
            "severity",
            "Low"
        )


        # AI Analysis

        ai_result = analyze_disaster(
            disaster,
            severity
        )


        report = {

            "report_id": report_id,

            "location": location,

            "disaster": disaster,

            "severity": severity,

            "ai_analysis": ai_result,

            "timestamp":
            str(datetime.datetime.now())

        }


        # Store in DynamoDB

        table.put_item(
            Item=report
        )


        return jsonify({

            "message":
            "Disaster report stored successfully",

            "data":
            report

        })


    except Exception as e:


        return jsonify({

            "error": str(e)

        }),500




# -----------------------------
# GET ALL REPORTS
# -----------------------------

@app.route("/reports")
def get_reports():

    try:

        response = table.scan()


        return jsonify(
            response["Items"]
        )


    except Exception as e:


        return jsonify({

            "error":str(e)

        }),500




# -----------------------------
# IMAGE UPLOAD
# -----------------------------

@app.route("/upload", methods=["POST"])
def upload_image():

    try:

        file = request.files["image"]


        filename = (
            str(uuid.uuid4())
            +
            file.filename
        )


        s3.upload_fileobj(
            file,
            S3_BUCKET,
            filename
        )


        return jsonify({

            "message":
            "Image uploaded",

            "file":
            filename

        })


    except Exception as e:


        return jsonify({

            "error":str(e)

        }),500




# -----------------------------
# START SERVER
# -----------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
