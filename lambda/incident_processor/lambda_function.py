import json
import boto3
import urllib.parse
import uuid
import datetime


s3 = boto3.client(
    "s3",
    region_name="ap-southeast-2"
)


dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-southeast-2"
)


table = dynamodb.Table(
    "incident-analysis"
)


def lambda_handler(event, context):

    print("EVENT:")
    print(json.dumps(event))


    for record in event["Records"]:

        bucket = record["s3"]["bucket"]["name"]

        key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )


        print("Bucket:")
        print(bucket)

        print("File:")
        print(key)


        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )


        data = json.loads(
            response["Body"].read().decode("utf-8")
        )


        print("JSON DATA:")
        print(json.dumps(data))


        incident_id = str(uuid.uuid4())


        item = {

            "incident_id": incident_id,

            "name": data.get(
                "name",
                "Unknown"
            ),

            "phone": data.get(
                "phone",
                "Unknown"
            ),

            "location": data.get(
                "location",
                "Unknown"
            ),

            "type": data.get(
                "type",
                "Unknown"
            ),

            "description": data.get(
                "description",
                "Unknown"
            ),

            "created_at": str(
                datetime.datetime.now()
            )

        }


        table.put_item(
            Item=item
        )


        print("Stored in DynamoDB")


    return {

        "statusCode": 200,

        "body": json.dumps(
            "Incident stored successfully"
        )

    }
