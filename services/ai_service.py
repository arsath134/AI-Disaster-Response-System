import boto3
import json

from config import (
    AWS_REGION,
    BEDROCK_MODEL_ID
)


bedrock = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION
)



def generate_ai_response(report):

    prompt = f"""

You are an emergency disaster response AI assistant.


Analyze this disaster.


Location:
{report['location']}


Disaster Type:
{report['type']}


Description:
{report['description']}



Return ONLY valid JSON:


{{
"severity":"",
"first_person_instruction":"",
"third_person_instruction":""
}}



Rules:

severity:
Choose LOW, MEDIUM, HIGH, or CRITICAL.


first_person_instruction:
Give instructions to the person who reported the disaster.

Start with:

"I should..."


third_person_instruction:
Give instructions for rescue teams and public.

Start with:

"The affected person should..."

"""


    response = bedrock.converse(

        modelId=BEDROCK_MODEL_ID,

        messages=[

            {
                "role":"user",

                "content":[
                    {
                        "text":prompt
                    }
                ]
            }

        ],

        inferenceConfig={

            "maxTokens":500,

            "temperature":0.2

        }

    )


    ai_text = response["output"]["message"]["content"][0]["text"]


    return json.loads(ai_text)
