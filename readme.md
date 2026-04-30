📌 Upwork Job Alert Pipeline (AWS Lambda + Serverless Scraper)

🚀 Overview
This project is a serverless job monitoring system that scrapes Upwork job listings at regular intervals and delivers real-time alerts to Discord.

It runs fully on AWS and is designed to demonstrate a production-style event-driven data pipeline using cloud services.

The system:
    Scrapes Upwork job listings using Zyte API
    Filters and detects new jobs using DynamoDB
    Sends formatted job alerts to Discord via webhook
    Runs automatically every 10 minutes using AWS EventBridge


EventBridge (Scheduler - every 10 minutes)
        ↓
AWS Lambda (Python runtime)
        ↓
Zyte API (Job page extraction)
        ↓
BeautifulSoup (HTML parsing)
        ↓
DynamoDB (Deduplication storage)
        ↓
Discord Webhook (Real-time notifications)


⚙️ Tech Stack
AWS Lambda – Serverless compute execution
Amazon EventBridge – Scheduled triggering (cron/rate-based)
Amazon DynamoDB – NoSQL database for deduplication
Python 3.x
BeautifulSoup4 – HTML parsing
Zyte API – Anti-bot web scraping service
Discord Webhooks – Real-time notifications

🧠 Key Features
⏱ Automated execution every 10 minutes
🔁 Duplicate job prevention using DynamoDB conditional writes
🧹 Structured job parsing using BeautifulSoup
📡 Real-time Discord notifications
☁️ Fully serverless, no server management required
💰 Low-cost cloud architecture (~$1–$2/month at small scale)

🏗 AWS Services Used
AWS Lambda (core compute logic)
Amazon EventBridge (scheduled triggers)
Amazon DynamoDB (job deduplication storage)
AWS IAM (permissions for Lambda execution & DynamoDB access)
Amazon CloudWatch (logging & monitoring)