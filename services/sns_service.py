import boto3


sns=boto3.client(
"sns"
)



def send_alert(topic,message):


    sns.publish(

        TopicArn=topic,

        Message=message

    )
