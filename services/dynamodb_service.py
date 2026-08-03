import boto3


dynamodb=boto3.resource(
"dynamodb"
)



def save_incident(data):


    table=dynamodb.Table(
    "incident-analysis"
    )


    table.put_item(

        Item=data

    )
