import boto3



sns=boto3.client(

    "sns",

    region_name="ap-southeast-2"

)



SNS_TOPIC_ARN="arn:aws:sns:ap-southeast-2:755642981171:disaster-alerts"




def lambda_handler(event,context):


    print(event)


    for record in event["Records"]:


        if record["eventName"]=="INSERT":


            data=record["dynamodb"]["NewImage"]



            severity=data["severity"]["S"]



            if severity in [
                "HIGH",
                "CRITICAL"
            ]:


                message=f"""

🚨 DISASTER ALERT 🚨


Location:

{data['location']['S']}



Disaster Type:

{data['type']['S']}



Severity:

{severity}



Reporter Safety:

{data['first_person']['S']}



Public / Rescue Instruction:

{data['third_person']['S']}

"""


                sns.publish(

                    TopicArn=SNS_TOPIC_ARN,

                    Subject="Emergency Disaster Alert",

                    Message=message

                )



    return {

        "status":"completed"

    }
