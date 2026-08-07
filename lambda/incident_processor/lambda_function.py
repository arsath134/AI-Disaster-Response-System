import json
import boto3
import uuid
import datetime


dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-southeast-2"
)


TABLE_NAME = "incident-analysis"


table = dynamodb.Table(TABLE_NAME)



def lambda_handler(event, context):

    print(json.dumps(event))


    try:

        body = json.loads(
            event["body"]
        )


        incident_id = str(uuid.uuid4())


        item = {

            "incident_id": incident_id,

            "name": body["name"],

            "phone": body["phone"],

            "location": body["location"],

            "type": body["type"],

            "description": body["description"],

            "timestamp":
            str(datetime.datetime.utcnow())

        }


        table.put_item(
            Item=item
        )


        return {

            "statusCode":200,

            "body":json.dumps({

                "message":
                "Emergency report submitted",

                "incident_id":
                incident_id

            })

        }



    except Exception as e:

        print(e)

        return {

            "statusCode":500,

            "body":
            json.dumps(
                str(e)
            )

        }
