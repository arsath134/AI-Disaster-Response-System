import json
import boto3
import os
import urllib.request
import urllib.error


# ============================================================
# AWS SNS CONFIGURATION
# ============================================================

sns = boto3.client(
    "sns",
    region_name="ap-southeast-2"
)

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


# ============================================================
# GROQ AI CONFIGURATION
# ============================================================

GROQ_API_KEY = os.environ["GROQ_API_KEY"]

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

GROQ_MODEL = "openai/gpt-oss-20b"


# ============================================================
# SEND EMAIL ALERT THROUGH SNS
# ============================================================

def send_alert(message, disaster_type):

    try:

        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,

            Subject=f"DISASTER EMERGENCY ALERT - {disaster_type.upper()}",

            Message=message
        )

        print("====================================")
        print("SNS EMAIL ALERT SENT")
        print("SNS Message ID:", response["MessageId"])
        print("====================================")

        return True

    except Exception as error:

        print("====================================")
        print("SNS ERROR")
        print("====================================")

        print(str(error))

        return False


# ============================================================
# GENERATE AI RESPONSE FOR RESCUE TEAMS
# ============================================================

def generate_ai_response(
    name,
    location,
    disaster_type,
    description
):

    print("====================================")
    print("CALLING GROQ AI")
    print("====================================")

    prompt = f"""
You are an AI emergency disaster-response assistant
helping emergency authorities and rescue teams.

Analyze the following disaster incident and provide
clear, practical and immediate guidance for responders.

INCIDENT INFORMATION

Person: {name}
Location: {location}
Disaster Type: {disaster_type}
Situation: {description}


YOUR RESPONSE MUST CONTAIN EXACTLY TWO SECTIONS.


SECTION 1 — RESCUE RESPONSE

Write this section from the perspective of emergency
responders.

Use language such as:

"Rescue teams should..."
"Responders should..."
"Emergency personnel should..."
"They should..."

Explain what responders should do immediately to:

1. Assess the reported situation.
2. Safely approach the affected location.
3. Assist the reported person.
4. Search for other potentially affected people.
5. Help vulnerable people when appropriate.
6. Coordinate evacuation when necessary.
7. Avoid hazards and unsafe areas.
8. Contact additional emergency services when required.


SECTION 2 — PRIORITY AND SAFETY

Explain the main priorities for responders.

Include:

- Immediate safety priorities.
- Important hazards to watch for.
- Whether additional emergency teams may be required.
- Safe coordination and evacuation considerations.
- Communication and monitoring recommendations.


IMPORTANT SAFETY RULES

- Prioritize human safety.
- Adapt the guidance to the reported disaster type.
- Do not invent facts that are not provided.
- Do not provide medical diagnosis.
- Do not recommend dangerous actions.
- Do not tell untrained people to enter dangerous areas.
- Do not assume that a location is safe.
- Recommend trained emergency personnel when appropriate.
- Keep instructions practical.
- Use simple English.
- Keep the response concise because it will be sent by email.
- Do not use tables.
- Do not add unnecessary explanations.
- Do not mention that you are an AI.


FORMAT THE RESPONSE EXACTLY LIKE THIS:

1. RESCUE RESPONSE

Rescue teams should ...
Responders should ...
They should ...


2. PRIORITY AND SAFETY

The priority should be ...
Responders should ...
Additional emergency assistance may be required if ...
"""


    payload = {

        "model": GROQ_MODEL,

        "messages": [

            {
                "role": "system",

                "content": (
                    "You are a professional emergency "
                    "disaster-response assistant helping "
                    "trained emergency responders. "
                    "Give concise, practical and "
                    "safety-focused guidance."
                )
            },

            {
                "role": "user",

                "content": prompt
            }

        ],

        "temperature": 0.2,

        "max_tokens": 500
    }


    request = urllib.request.Request(

        GROQ_URL,

        data=json.dumps(
            payload
        ).encode("utf-8"),

        headers={

            "Content-Type":
            "application/json",

            "Authorization":
            f"Bearer {GROQ_API_KEY}"
        },

        method="POST"
    )


    try:

        with urllib.request.urlopen(
            request,
            timeout=20
        ) as response:

            response_body = (
                response
                .read()
                .decode("utf-8")
            )


        response_data = json.loads(
            response_body
        )


        ai_response = (
            response_data
            ["choices"]
            [0]
            ["message"]
            ["content"]
        )


        print("====================================")
        print("AI RESPONSE GENERATED")
        print("====================================")

        print(ai_response)

        return ai_response


    except urllib.error.HTTPError as error:

        print("====================================")
        print("GROQ HTTP ERROR")
        print("====================================")

        print("HTTP Status:", error.code)

        try:

            error_body = (
                error
                .read()
                .decode("utf-8")
            )

            print("Error Response:")
            print(error_body)

        except Exception:

            print(
                "Could not read error response."
            )


        return (
            "1. RESCUE RESPONSE\n\n"
            "Rescue teams should assess the reported "
            "location and safely assist the affected "
            "person. Responders should check whether "
            "other people may also be affected and "
            "avoid entering unsafe areas without "
            "appropriate equipment.\n\n"
            "2. PRIORITY AND SAFETY\n\n"
            "The priority should be protecting people "
            "from immediate hazards and coordinating "
            "appropriate emergency assistance."
        )


    except Exception as error:

        print("====================================")
        print("GROQ AI ERROR")
        print("====================================")

        print(str(error))


        return (
            "1. RESCUE RESPONSE\n\n"
            "Rescue teams should assess the reported "
            "location and safely assist the affected "
            "person. Responders should check whether "
            "other people may also be affected and "
            "avoid entering unsafe areas without "
            "appropriate equipment.\n\n"
            "2. PRIORITY AND SAFETY\n\n"
            "The priority should be protecting people "
            "from immediate hazards and coordinating "
            "appropriate emergency assistance."
        )


# ============================================================
# EXTRACT DYNAMODB STRING VALUE
# ============================================================

def get_string_value(
    new_image,
    field_name,
    default_value
):

    return (
        new_image
        .get(
            field_name,
            {}
        )
        .get(
            "S",
            default_value
        )
    )


# ============================================================
# LAMBDA HANDLER
# ============================================================

def lambda_handler(event, context):

    print("====================================")
    print("DISASTER NOTIFICATION LAMBDA")
    print("AI-POWERED AUTHORITY ALERT VERSION")
    print("====================================")


    print("EVENT:")

    print(
        json.dumps(
            event
        )
    )


    records = event.get(
        "Records",
        []
    )


    print(
        "Number of records:",
        len(records)
    )


    # ========================================================
    # PROCESS EACH DYNAMODB STREAM RECORD
    # ========================================================

    for record in records:

        print("====================================")
        print("PROCESSING RECORD")
        print("====================================")


        event_name = record.get(
            "eventName"
        )


        print(
            "Event name:",
            event_name
        )


        # ----------------------------------------------------
        # ONLY PROCESS INSERT EVENTS
        # ----------------------------------------------------

        if event_name != "INSERT":

            print(
                "Skipping event:",
                event_name
            )

            continue


        dynamodb_data = record.get(
            "dynamodb",
            {}
        )


        new_image = dynamodb_data.get(
            "NewImage",
            {}
        )


        if not new_image:

            print(
                "NewImage is empty. "
                "Skipping record."
            )

            continue


        # ====================================================
        # READ INCIDENT DATA
        # ====================================================

        incident_id = get_string_value(
            new_image,
            "incident_id",
            "UNKNOWN"
        )


        name = get_string_value(
            new_image,
            "name",
            "Unknown"
        )


        phone = get_string_value(
            new_image,
            "phone",
            "Unknown"
        )


        location = get_string_value(
            new_image,
            "location",
            "Unknown"
        )


        disaster_type = get_string_value(
            new_image,
            "type",
            "Unknown"
        )


        description = get_string_value(
            new_image,
            "description",
            "No description"
        )


        created_at = get_string_value(
            new_image,
            "created_at",
            "Unknown"
        )


        # ====================================================
        # PRINT INCIDENT INFORMATION
        # ====================================================

        print("====================================")
        print("INCIDENT INFORMATION")
        print("====================================")


        print(
            "Incident ID:",
            incident_id
        )


        print(
            "Name:",
            name
        )


        print(
            "Phone:",
            phone
        )


        print(
            "Location:",
            location
        )


        print(
            "Disaster Type:",
            disaster_type
        )


        print(
            "Description:",
            description
        )


        print(
            "Created At:",
            created_at
        )


        # ====================================================
        # CALL AI
        # ====================================================

        ai_response = generate_ai_response(

            name=name,

            location=location,

            disaster_type=disaster_type,

            description=description
        )


        # ====================================================
        # CREATE AUTHORITY EMAIL
        # ====================================================

        message = f"""
🚨 DISASTER EMERGENCY ALERT
====================================

INCIDENT INFORMATION
====================================

Incident ID:
{incident_id}

Affected Person:
{name}

Contact Phone:
{phone}

Location:
{location}

Disaster Type:
{disaster_type}

Situation:
{description}

Reported At:
{created_at}


====================================
AI EMERGENCY RESPONSE
====================================

{ai_response}


====================================
RESPONSE REQUIRED
====================================

Please assess the reported incident
and coordinate appropriate emergency
assistance.

Responders should follow their official
emergency procedures and use appropriate
safety equipment.

====================================
SYSTEM NOTICE
====================================

This alert was generated automatically
from the AI Disaster Response System.

AI-generated guidance should support,
not replace, instructions from qualified
emergency authorities.
"""


        # ====================================================
        # PRINT FINAL EMAIL
        # ====================================================

        print("====================================")
        print("FINAL AUTHORITY EMAIL")
        print("====================================")


        print(
            message
        )


        # ====================================================
        # SEND EMAIL THROUGH SNS
        # ====================================================

        sns_success = send_alert(
            message,
            disaster_type
        )


        if sns_success:

            print(
                "Authority notification completed for:",
                incident_id
            )

        else:

            print(
                "Authority notification failed for:",
                incident_id
            )


    # ========================================================
    # LAMBDA RESPONSE
    # ========================================================

    return {

        "statusCode": 200,

        "body": json.dumps(
            {
                "message":
                "AI disaster authority notification completed successfully"
            }
        )
    }
