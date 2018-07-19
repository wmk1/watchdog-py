import os

import boto3
import subprocess
from time import sleep


AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
table_name="rnd-coding-challenge-wojciechmkalinski-gmailcom-WatchdogTable-1T6M0MOPDKMI2"
topic_arn="rnd-coding-challenge-wojciechmkalinski-gmailcom-WatchdogSnsTopic-YYX9A9SCNG2Z"

sns = boto3.client("sns", region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY,
                   aws_secret_access_key=AWS_SECRET_KEY)
dynamodb = boto3.resource('dynamodb')
watchdog_table = dynamodb.Table(table_name)
array_of_services = ['spotify', 'java']


def insert_row():
    watchdog_table.put_item(
        Item={
            'id': "1",
            'ListOfServices': ["spotify", "java"],
            'NumOfSecCheck': '60',
            'NumOfSecWait': '10',
            'NumOfAttempts': '4'
        }
    )


def publish_sns(message):
    sns.publish(
        TargetArn=topic_arn,
        Message=message
    )


def check_services(id):
    response = watchdog_table.get_item(
        TableName=table_name,
        Key={
            'id': id
        }
    )
    item = response['Item']
    num_of_sec_check = item['NumOfSecCheck']
    num_of_sec_wait = item['NumOfSecWait']
    num_of_attempts = item['NumOfAttempts']
    services = item['ListOfServices']
    p = subprocess.Popen(["ps", "-a"], stdout=subprocess.PIPE)
    attempts = 0
    out, err = p.communicate()
    for service in services:
        if service in str(out):
            publish_sns(service + " has been started after " + attempts + " attempts." )
        else:
            while attempts < num_of_attempts:
                attempts += 1
                publish_sns(service + " is not running after " + attempts + " attempts.")
                sleep(num_of_sec_wait)
                continue
            if attempts >= num_of_attempts:
                publish_sns(service + " is down.")
        sleep(num_of_sec_check)


def main(row_id):
    insert_row()
    check_services(row_id)


main(1)