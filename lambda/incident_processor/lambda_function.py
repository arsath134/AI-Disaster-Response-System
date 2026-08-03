import json
import boto3
import urllib.parse
from datetime import datetime


s3 = boto3.client("s3")

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-southeast-2"
)

table = dynamodb.Table(
    "incident-analysis"
)



def analyze_disaster(description):

    text = description.lower()

    if "fire" in text:
        return "CRITICAL"

    elif "flood" in text:
        return "HIGH"

    elif "earthquake" in text:
        return "CRITICAL"

    elif "storm" in text:
        return "HIGH"

    else:
        return "LOW"



def lambda_handler(event, context):

    record = event["Records"][0]


    bucket = record["s3"]["bucket"]["name"]

    key = urllib.parse.unquote_plus(
        record["s3"]["object"]["key"]
    )


    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )


    report = json.loads(
        response["Body"].read()
    )


    severity = analyze_disaster(
        report["description"]
    )


    item = {

        "report": key,

        "location": report["location"],

        "type": report["type"],

        "description": report["description"],

        "severity": severity,

        "status": "OPEN",

        "time": datetime.now().isoformat()

    }


    table.put_item(
        Item=item
    )


    return {

        "statusCode":200,

        "body":
        json.dumps(item)

    }
