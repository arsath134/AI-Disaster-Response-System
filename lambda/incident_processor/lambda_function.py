import json
import boto3
from datetime import datetime


dynamodb=boto3.resource("dynamodb")


table=dynamodb.Table(
"incident-analysis"
)



def lambda_handler(event,context):


    record=event["Records"][0]


    bucket=record["s3"]["bucket"]["name"]

    file=record["s3"]["object"]["key"]


    result={

        "report":file,

        "severity":"HIGH",

        "analysis":
        "Emergency situation detected",

        "time":
        datetime.now().isoformat()

    }



    table.put_item(

        Item=result

    )


    return {


        "statusCode":200,

        "body":
        json.dumps(result)

    }
