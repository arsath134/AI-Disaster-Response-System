import json
import boto3
import urllib.parse
from datetime import datetime


s3 = boto3.client("s3")

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="ap-southeast-2"
)


dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-southeast-2"
)


table = dynamodb.Table("incident-analysis")



def lambda_handler(event, context):

    print("===== INCIDENT PROCESSOR START =====")


    record = event["Records"][0]


    bucket = record["s3"]["bucket"]["name"]

    key = urllib.parse.unquote_plus(
        record["s3"]["object"]["key"]
    )


    print("Bucket:", bucket)
    print("File:", key)



    # Read report from S3

    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )


    report = json.loads(
        response["Body"].read().decode("utf-8")
    )


    print("REPORT:")
    print(report)



    # =========================
    # BEDROCK AI
    # =========================


    prompt = f"""

You are an AI Disaster Response Assistant.

Analyze this emergency report.

Location:
{report['location']}

Disaster Type:
{report['type']}

Description:
{report['description']}


Return ONLY JSON:

{{
"severity":"",
"first_person":"",
"third_person":""
}}

first_person:
Give instructions directly to the affected citizen.

third_person:
Give instructions for rescue teams and public.

"""


    bedrock_response = bedrock.invoke_model(

        modelId="amazon.nova-lite-v1:0",

        body=json.dumps({

            "messages":[

                {

                "role":"user",

                "content":[

                    {
                    "text":prompt
                    }

                ]

                }

            ],

            "inferenceConfig":{

                "maxTokens":300,

                "temperature":0.3

            }

        }),

        contentType="application/json",

        accept="application/json"

    )



    result = json.loads(
        bedrock_response["body"].read()
    )



    ai_text = result["output"]["message"]["content"][0]["text"]



    start = ai_text.find("{")

    end = ai_text.rfind("}") + 1


    ai_result = json.loads(
        ai_text[start:end]
    )



    # =========================
    # STORE IN DYNAMODB
    # =========================


    item = {


        "report":key,


        "name":report.get("name","Unknown"),


        "email":report.get("email",""),


        "location":report["location"],


        "type":report["type"],


        "description":report["description"],


        "severity":ai_result["severity"],


        "first_person":ai_result["first_person"],


        "third_person":ai_result["third_person"],


        "status":"OPEN",


        "time":datetime.now().isoformat()

    }



    table.put_item(
        Item=item
    )


    print("DynamoDB Insert Completed")


    return {

        "statusCode":200,

        "body":json.dumps(item)

    }
