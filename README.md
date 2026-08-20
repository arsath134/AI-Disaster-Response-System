# 🚨 AI Disaster Response System

An AWS-based disaster response system that helps process disaster reports and automatically notify emergency authorities with AI-powered response guidance.

The main goal of this project is to reduce the time between reporting a disaster and informing the right people who can respond.

## 📌 How It Works

1. A citizen submits a disaster report with details such as name, phone number, location, disaster type, and description.
2. The incident is stored in Amazon DynamoDB.
3. DynamoDB Streams detects the new incident.
4. AWS Lambda processes the incident.
5. Groq AI analyzes the disaster information and generates practical guidance for rescue teams.
6. Amazon SNS sends the emergency alert to the subscribed authority email.
7. Emergency teams can use the incident details to coordinate the required response.

                                                    ## 🏗️ AWS Architecture

                                                           Citizen
   │
   ▼
Web Application
   │
   ▼
Amazon DynamoDB
   │
   ▼
DynamoDB Streams
   │
   ▼
AWS Lambda
   │
   ├──────────────► Groq AI
   │                    │
   │                    ▼
   │             Emergency Guidance
   │
   ▼
Amazon SNS
   │
   ▼
📧 Emergency Authority

## ☁️ AWS Services Used

- Amazon DynamoDB – Stores disaster incident information.
- DynamoDB Streams – Detects newly created incidents.
- AWS Lambda – Processes incidents and coordinates the workflow.
- Amazon SNS – Sends emergency notifications through email.
- Amazon S3 – Used for storing project-related files/data where required.
- Amazon CloudWatch – Used for Lambda logs and monitoring.
- AWS IAM – Controls access between AWS services.
- Amazon VPC – Provides the required AWS networking environment.

## 🤖 AI Integration

The system uses Groq AI to analyze the reported disaster and generate concise guidance for emergency responders.

The AI response focuses on:

- Rescue response
- Immediate safety priorities
- Possible hazards
- Assistance for affected people
- Coordination with additional emergency teams
- Safe evacuation considerations

The AI provides supporting guidance and does not replace instructions from qualified emergency authorities.

## 📧 Emergency Notifications

The generated response is included in an emergency alert containing:

- Incident ID
- Affected person's name
- Contact phone number
- Location
- Disaster type
- Situation description
- Reported time
- AI-generated emergency guidance

The alert is delivered through an Amazon SNS email subscription.

## 🛠️ Technologies

Cloud: AWS
AI: Groq API
Backend: Python / AWS Lambda
Database: Amazon DynamoDB
Notifications: Amazon SNS
Monitoring: Amazon CloudWatch
Security: AWS IAM
Networking: Amazon VPC

## 🎯 Project Goal

This project was built as a practical AWS cloud project to understand how different AWS services can work together in an event-driven architecture.

The system can be extended in the future with automatic routing to specific emergency teams such as:

- 🚒 Fire Stations
- 🚑 Ambulance Services
- 🚔 Police
- 🚤 Boat / Water Rescue Teams

## 📚 What I Learned

Through this project, I worked with:

- Event-driven AWS architecture
- DynamoDB Streams
- Lambda functions
- SNS notifications
- IAM permissions
- CloudWatch monitoring
- API integration
- AI integration with AWS workflows
- Building automated cloud-based response systems

---

Built as an AWS learning project focused on cloud architecture, automation, AI integration, and disaster-response workflows.
