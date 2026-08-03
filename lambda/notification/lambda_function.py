import boto3


sns = boto3.client(
    "sns",
    region_name="ap-southeast-2"
)


SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"


def lambda_handler(event, context):

    for record in event["Records"]:

        if record["eventName"] == "INSERT":

            data = record["dynamodb"]["NewImage"]

            severity = data["severity"]["S"]


            if severity in ["HIGH", "CRITICAL"]:

                message = f"""
🚨 DISASTER ALERT 🚨

Location:
{data['location']['S']}

Type:
{data['type']['S']}

Severity:
{severity}

Description:
{data['description']['S']}
"""


                sns.publish(

                    TopicArn=SNS_TOPIC_ARN,

                    Subject="Emergency Disaster Alert",

                    Message=message

                )


    return {

        "statusCode": 200,

        "body": "Notification completed"

    }
