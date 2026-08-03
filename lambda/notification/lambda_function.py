import boto3


sns=boto3.client(
"sns"
)



TOPIC_ARN="YOUR_TOPIC_ARN"



def lambda_handler(event,context):


    sns.publish(

        TopicArn=TOPIC_ARN,

        Message=
        "Emergency Disaster Alert Generated"

    )


    return {


        "status":
        "Notification Sent"

    }
