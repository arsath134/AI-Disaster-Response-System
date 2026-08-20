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
# SEND SNS ALERT
# ============================================================

def send_alert(message):

    try:

        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="DISASTER EMERGENCY ALERT",
            Message=message
        )

        print("====================================")
        print("SNS MESSAGE SENT")
        print("SNS Message ID:", response["MessageId"])
        print("====================================")

        return True

    except Exception as error:

        print("====================================")
        print("SNS ERROR")
        print(str(error))
        print("====================================")

        return False


# ============================================================
# GENERATE AI EMERGENCY RESPONSE
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
You are an AI emergency disaster response assistant.

Analyze the following disaster incident and provide
clear, practical and immediate emergency guidance.

INCIDENT INFORMATION

Person: {name}
Location: {location}
Disaster Type: {disaster_type}
Situation: {description}


YOUR RESPONSE MUST CONTAIN EXACTLY TWO SECTIONS.


SECTION 1 — AFFECTED PERSON

This section must be written from the affected person's
FIRST-PERSON perspective.

Use language such as:

"I should..."
"I must..."
"I need to..."
"I should avoid..."

Explain what the affected person should do immediately
to protect themselves and stay safe.

The instructions must be practical and appropriate for
the reported disaster.


SECTION 2 — RESCUE TEAMS AND HELPERS

This section must be written in THIRD-PERSON perspective.

Use language such as:

"Rescue teams should..."
"Responders should..."
"Helpers should..."
"They should..."

Explain what rescue teams, emergency responders,
neighbors, or other helpers can do to:

1. Help the affected person.
2. Check for other people who may also be affected.
3. Help vulnerable people when appropriate.
4. Perform safe evacuation when appropriate.
5. Avoid hazards while helping.
6. Coordinate emergency assistance when necessary.


IMPORTANT SAFETY RULES

- Prioritize immediate safety.
- Adapt the instructions to the disaster type.
- Do not invent facts that are not provided.
- Do not provide medical diagnosis.
- Do not recommend dangerous actions.
- Do not tell untrained people to enter dangerous areas.
- Keep instructions practical.
- Use simple English.
- Keep the response concise because it may be sent by SMS.
- Do not use tables.
- Do not add unnecessary explanations.
- Do not mention that you are an AI.


FORMAT THE RESPONSE EXACTLY LIKE THIS:

1. AFFECTED PERSON

I should ...
I should ...
I must ...

2. RESCUE TEAMS AND HELPERS

Rescue teams should ...
They should ...
Helpers should ...
"""


    payload = {
        "model": GROQ_MODEL,

        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional emergency "
                    "disaster-response assistant. "
                    "Give concise and safety-focused guidance."
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
            "Content-Type": "application/json",
            "Authorization": (
                f"Bearer {GROQ_API_KEY}"
            )
        },

        method="POST"
    )


    try:

        with urllib.request.urlopen(
            request,
            timeout=20
        ) as response:

            response_body = response.read().decode(
                "utf-8"
            )

        response_data = json.loads(
            response_body
        )


        ai_response = (
            response_data[
                "choices"
            ][
                0
            ][
                "message"
            ][
                "content"
            ]
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

            error_body = error.read().decode(
                "utf-8"
            )

            print("Error Response:")
            print(error_body)

        except Exception:

            print(
                "Could not read error response."
            )


        return (
            "1. AFFECTED PERSON\n\n"
            "I should move to a safe location if possible. "
            "I should avoid immediate hazards and keep my "
            "phone available for emergency communication.\n\n"
            "2. RESCUE TEAMS AND HELPERS\n\n"
            "Rescue teams should assess the reported location "
            "and safely assist the affected person. They should "
            "also check whether other people nearby need help."
        )


    except Exception as error:

        print("====================================")
        print("GROQ AI ERROR")
        print("====================================")

        print(str(error))


        return (
            "1. AFFECTED PERSON\n\n"
            "I should move to a safe location if possible. "
            "I should avoid immediate hazards and keep my "
            "phone available for emergency communication.\n\n"
            "2. RESCUE TEAMS AND HELPERS\n\n"
            "Rescue teams should assess the reported location "
            "and safely assist the affected person. They should "
            "also check whether other people nearby need help."
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
    print("AI-POWERED VERSION")
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
        # CREATE FINAL SMS
        # ====================================================

        message = f"""
DISASTER EMERGENCY ALERT

Incident ID:
{incident_id}

Person:
{name}

Phone:
{phone}

Location:
{location}

Disaster Type:
{disaster_type}

Situation:
{description}

Reported At:
{created_at}

================================
AI EMERGENCY RESPONSE
================================

{ai_response}

================================
SYSTEM NOTICE
================================

AI-generated emergency guidance.
Follow instructions from qualified
emergency responders when available.
"""


        # ====================================================
        # PRINT FINAL ALERT
        # ====================================================

        print("====================================")
        print("FINAL ALERT MESSAGE")
        print("====================================")


        print(
            message
        )


        # ====================================================
        # SEND SNS
        # ====================================================

        sns_success = send_alert(
            message
        )


        if sns_success:

            print(
                "Notification completed for:",
                incident_id
            )

        else:

            print(
                "Notification failed for:",
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
                "AI disaster notification completed successfully"
            }
        )
    }
