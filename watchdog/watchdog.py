import os

import boto3
import subprocess

from time import sleep

AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

sns = boto3.client("sns", region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY,
                   aws_secret_access_key=AWS_SECRET_KEY)
dynamodb = boto3.client('dynamodb')

array_of_services = ['spotify', 'java']


def insert_dynamodb_row():
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


def check_services(num_of_sec_wait=5, num_of_attempts=4):
    p = subprocess.Popen(["ps", "-a"], stdout=subprocess.PIPE)
    attempts = 0
    out, err = p.communicate()
    for service in array_of_services:
        if service in str(out):
            print(service + " running")
        else:
            while attempts < num_of_attempts:
                sleep(num_of_sec_wait)
                attempts += 1
                break
