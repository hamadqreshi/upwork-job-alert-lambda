import os
import time
import json
import http.client
from urllib.parse import urlparse
from base64 import b64encode, b64decode
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import ClientError


ZYTE_API_KEY = os.environ["ZYTE_API_KEY"]
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]
TABLE_NAME = os.environ.get("TABLE_NAME")
REGION = os.environ.get("AWS_REGION")
UPWORK_SEARCH_URL = os.environ.get("UPWORK_SEARCH_URL")
GEO_LOCATION = os.environ.get("GEO_LOCATION")

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)


def get_jobs_page():
    try:
        conn = http.client.HTTPSConnection("api.zyte.com")

        payload = json.dumps({
            "url": UPWORK_SEARCH_URL,
            "httpResponseBody": True,
            "geolocation": GEO_LOCATION
        })

        auth = b64encode(f"{ZYTE_API_KEY}:".encode("utf-8")).decode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}"
        }

        conn.request(
            "POST",
            "/v1/extract",
            body=payload,
            headers=headers
        )

        response = conn.getresponse()

        if response.status != 200:
            print(f"ZYTE ERROR: {response.status} {response.reason}")
            return None

        response_json = json.loads(
            response.read().decode("utf-8")
        )

        body = b64decode(response_json["httpResponseBody"])

        return BeautifulSoup(body, "html.parser")

    except Exception as e:
        print("ZYTE ERROR:", str(e))
        return None


def is_new_job(data):
    try:
        table.put_item(
            Item={
                "url": data["url"],
                "title": data.get("title", ""),
                "timestamp": int(time.time())
            },
            ConditionExpression="attribute_not_exists(#u)",
            ExpressionAttributeNames={
                "#u": "url"
            }
        )
        return True

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return False
        else:
            print("DYNAMODB ERROR:", e)
            return False


def format_job(data):
    return (
        f"**🔗 URL:** {data.get('url','')}\n"
        f"**📌 Title:** {data.get('title','')}\n"
        f"**✨ Description:** {data.get('description','')[:200]}...\n"
        f"**💰 Worth:** {data.get('worth','')}\n"
        f"**🕒 Time:** {data.get('time','')}\n"
        f"**🏷 Tags:** {data.get('hashtags','')}\n"
        f"\n──────────────────────────\n"
    )


def send_to_discord(messages):
    if not messages:
        return

    parsed = urlparse(DISCORD_WEBHOOK)

    conn = http.client.HTTPSConnection(parsed.netloc)

    for msg in messages:
        payload = json.dumps({"content": msg})

        conn.request(
            "POST",
            parsed.path,
            body=payload,
            headers={"Content-Type": "application/json"}
        )

        response = conn.getresponse()
        response.read()
        print("Discord response:", response.status)
        time.sleep(1)

    conn.close()


def crawler():
    soup = get_jobs_page()
    if not soup:
        return

    jobs = soup.select('[data-ev-label="search_result_impression"] article')

    messages = []

    for job in jobs:
        data = {}

        data['title'] = job.select_one('h2 a').get_text(strip=True)
        data['url'] = 'https://upwork.com' + job.select_one('h2 a').get('href')

        data['description'] = job.select_one('[class="mb-0 text-body-sm rr-mask"]').get_text(strip=True, separator=' ')
        data['worth'] = job.select_one('.job-tile-info-list').get_text(strip=True, separator=' ')
        data['time'] = job.select_one('[data-test="job-pubilshed-date"]').get_text(strip=True, separator=' ')
        data['hashtags'] = " | ".join(i.get_text(strip=True) for i in job.select('[class="air3-token-wrap"]'))

        if is_new_job(data):
            messages.append(format_job(data))

    print(f"Total jobs: {len(jobs)} | New jobs: {len(messages)}")
    send_to_discord(messages)


def lambda_handler(event, context):
    crawler()
    return {
        "statusCode": 200,
        "body": json.dumps("Done")
    }