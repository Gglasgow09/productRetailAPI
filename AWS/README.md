# E-commerce Analytics Platform Using AWS Free Tier

## Table of Contents
- [Overview](#overview)
- [Contributors](#contributors)
- [Requirements](#requirements)
- [Deliverables](#deliverables)
- [Timeline](#timeline)

## Overview

This project extends the functionality of the Retail API by integrating a serverless analytics platform on AWS Free Tier. The platform captures, processes, and visualizes transactional data to provide actionable insights into customer behavior and product performance without incurring additional costs.

## Contributors

Gabrielle Glasgow, Jason Fearnell, Justin Quinn, Max Ross

## Requirements

1. **Data Collection and Storage**: Design and implement a DynamoDB schema to efficiently store data about users, transactions, and products. Ensure the schema supports the queries needed for analytics.

2. **Data Processing with AWS Lambda**: Develop Lambda functions to perform ETL (Extract, Transform, Load) tasks on the data collected from the Retail API, preparing it for analytics. This includes data validation, transformation, and loading into DynamoDB.

3. **Analytics and Visualization**: Utilize CloudWatch for basic monitoring of application and Lambda function metrics, setting up simple dashboards for real-time monitoring.

4. **Integration and Security**: Utilize IAM for managing access permissions to the DynamoDB data, Lambda functions, and any other resources, enforcing the principle of least privilege.

## Extensions

5. **Data Processing with AWS Lambda**: Set up triggers using Amazon CloudWatch Events or S3 event notifications to automatically start data processing workflows.

6. **Analytics and Visualization**: Deploy an open-source visualization tool such as Apache Superset or Redash on a free tier EC2 instance. Connect this tool to DynamoDB (via custom APIs if necessary) to create interactive dashboards for business insights.

7. **Integration and Security**: Create RESTful endpoints with API Gateway that serve the processed data from DynamoDB to the visualization tools, ensuring data can be retrieved securely.

## Deliverables

- A serverless data processing architecture utilizing AWS Lambda and DynamoDB.
- A set of secure APIs for data access, built with Amazon API Gateway. (Extension)
- A hosted visualization tool on EC2, connected to DynamoDB, showcasing interactive dashboards. (Extension)

## Timeline

3 weeks

