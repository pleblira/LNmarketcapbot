import boto3
from dotenv import load_dotenv, find_dotenv
import os
import json
from datetime import date, timedelta

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

def s3_update_LN_capacity_and_compare(LN_capacity_in_BTC):
    # creating dictionary to dump jsons in
    LN_capacity_by_day = []

    # today's date
    today_in_yyyymmdd = f"{date.today():%Y%m%d}"
    # downloading LN capacity history file from S3 bucket
    boto3.client('s3').download_file('pleblira', 'LN_capacity_by_day.json', 'assets/LN_capacity_by_day.json')


    # appending today's capacity to json file
    with open('assets/LN_capacity_by_day.json', 'r+') as openfile:
        LN_capacity_by_day = json.load(openfile)
        LN_capacity_by_day.append({"date":today_in_yyyymmdd,"capacity":LN_capacity_in_BTC})
        openfile.seek(0)
        openfile.write(json.dumps(LN_capacity_by_day, indent=4))

    # overwriting history file back to S3
    s3_upload = boto3.resource(
        's3',
        region_name='us-east-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    content=json.dumps(LN_capacity_by_day).encode('utf-8')
    s3_upload.Object('pleblira', 'LN_capacity_by_day.json').put(Body=content,ACL="public-read")

    # getting LN capacity from a week ago
    for value in LN_capacity_by_day:
        if value['date'] == f"{date.today() + timedelta(days=-7):%Y%m%d}":
            LN_capacity_in_BTC_a_week_ago = value['capacity']

    LN_capacity_percentage_change = f"{(100 * (LN_capacity_in_BTC - int(LN_capacity_in_BTC_a_week_ago))/int(LN_capacity_in_BTC_a_week_ago)):+.2f}"
    LN_capacity_weekly_change_text = (f"LN capacity change from last week: {LN_capacity_percentage_change.rstrip('0').rstrip('.')}%")
    print(LN_capacity_weekly_change_text)
    return LN_capacity_weekly_change_text


# if __name__ == '__main__':
    # s3_update_LN_capacity_and_compare(3999)