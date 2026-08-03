import os

class Config:

    AWS_REGION = "ap-southeast-2"

    S3_BUCKET = "ai-disaster-uploads"

    DYNAMODB_TABLE = "IncidentReports"

    SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"

    AI_PROVIDER = "groq"

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MAX_UPLOAD_SIZE = 20 * 1024 * 1024
