# Upwork Job Alert Lambda – Setup Guide

This document explains how to set up and run the Upwork Job Alert system on AWS Lambda.

---

## 🚀 Overview

This project scrapes Upwork job listings, filters new jobs, stores them in DynamoDB, and sends alerts to Discord using AWS Lambda scheduled every 10 minutes via EventBridge.

---

## 🧱 AWS Services Used

- AWS Lambda (main execution)
- Amazon EventBridge (10-minute trigger)
- Amazon DynamoDB (deduplication storage)
- IAM (permissions for Lambda execution)

---

## ⚙️ Environment Variables

Before deploying, configure the following environment variables in Lambda:

| Variable Name        | Description                          |
|---------------------|--------------------------------------|
| ZYTE_API_KEY        | API key for Zyte scraping service    |
| DISCORD_WEBHOOK     | Discord webhook URL for alerts       |
| TABLE_NAME          | DynamoDB table name                  |
| AWS_REGION          | AWS region (e.g. us-east-1)         |
| UPWORK_SEARCH_URL   | Upwork search URL to scrape         |
| GEO_LOCATION        | Zyte geolocation (optional)          |

---

## 🗄️ DynamoDB Setup

Create a table:

- Table Name: `upwork_jobs`
- Partition Key: `url` (String)

This ensures each job is stored only once.

---

## 🔐 IAM Permissions

Attach this policy to the Lambda execution role:

```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:PutItem",
    "dynamodb:GetItem",
    "dynamodb:UpdateItem",
    "dynamodb:Query",
    "dynamodb:Scan"
  ],
  "Resource": "arn:aws:dynamodb:REGION:ACCOUNT_ID:table/upwork_jobs"
}