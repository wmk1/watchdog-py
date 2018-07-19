This project contains python script, which uses boto3 library to watch Linux services, and send notifications to SNS.

How to run it:

    * cd/to/your/repo
    * python watchdog.py -x
Where x is an id of row, which contains information about services, which watchdog is going to check through system.

AWS credentials are stored as envkey, therefore no credentials are visible in script.

