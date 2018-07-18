import os

import boto3
import subprocess
import json
from botocore.exceptions import ClientError

from time import sleep

import daemon

AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

sns = boto3.client("sns", region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY,
                   aws_secret_access_key=AWS_SECRET_KEY)
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
watchdog_table = dynamodb.Table("rnd-coding-challenge-wojciechmkalinski-gmailcom-WatchdogTable-1T6M0MOPDKMI2")
array_of_services = ['spotify', 'java']


def insert_row():
    dynamodb.put_item(
        TableName="rnd-coding-challenge-wojciechmkalinski-gmailcom-WatchdogTable-1T6M0MOPDKMI2",
        Item={
            'Id': "1",
            'ListOfServices': ["mysqld", "java"],
            'NumOfSecCheck': 60,
            'NumOfSecWait': 10,
            'NumOfAttempts': 4
        }
    )


def check_services(row):
    num_of_sec_wait = row.NumOfSecWait
    num_of_attempts = row.NumOfAttempts
    p = subprocess.Popen(["ps", "-a"], stdout=subprocess.PIPE)
    attempts = 0
    out, err = p.communicate()
    for service in array_of_services:
        if service in str(out):
            sns.publish(
                TargetArn="rnd-coding-challenge-wojciechmkalinski-gmailcom-WatchdogSnsTopic-YYX9A9SCNG2Z",
                Message=json.dumps()
            )
            print(service + " running")
        else:
            while attempts < num_of_attempts:
                attempts += 1
                print(attempts + " check of " + service + " not running.")
                sleep(num_of_sec_wait)


def get_row():
    try:
        response = watchdog_table.get_item(
            Key={
                'Id': '1'
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        item = response('Item')
    return item


def main():
    insert_row()
    db_row = get_row()
    check_services(db_row)
