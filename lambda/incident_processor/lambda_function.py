import json
import boto3
import urllib.parse
from datetime import datetime


from services.ai_service import generate_ai_response



s3=boto3.client(
    "s3"
)



dynamodb=boto3.resource(
    "dynamodb",
    region_name="ap-southeast-2"
)



table=dynamodb.Table(
    "incident-analysis"
)




def lambda_handler(event,context):


    print("EVENT:")
    print(json.dumps(event))


    record=event["Records"][0]


    bucket=record["s3"]["bucket"]["name"]


    key=urllib.parse.unquote_plus(

        record["s3"]["object"]["key"]

    )



    print("Bucket:",bucket)

    print("File:",key)



    response=s3.get_object(

        Bucket=bucket,

        Key=key

    )


    report=json.loads(

        response["Body"].read()

    )


    print("REPORT:")
    print(report)



    ai_result=generate_ai_response(report)



    print("AI RESULT:")
    print(ai_result)



    item={


        "report":key,


        "location":
        report["location"],



        "type":
        report["type"],



        "description":
        report["description"],



        "severity":
        ai_result["severity"],



        "first_person":
        ai_result["first_person_instruction"],



        "third_person":
        ai_result["third_person_instruction"],



        "status":
        "OPEN",



        "time":
        datetime.now().isoformat()

    }



    table.put_item(

        Item=item

    )



    return {

        "statusCode":200,

        "body":
        json.dumps(item)

    }
