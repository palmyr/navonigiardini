import os
import re
import json
import boto3
import requests

CHARSET = "UTF-8"

sesClient = boto3.client('ses',region_name=os.environ.get('AWS_REGION'))

def lambda_handler(event, context):
    print("handling call [Event: {} ] [Context: {} ] ".format(event, context))

    data = json.loads(event['body'])

    print("data [ {} ]".format(data))

    response = {}

    try:
        validateCaptcha(data['g-recaptcha-response'])

    except Exception as error:
        print("Error [ {} ]".format(error))
        response["message"] = str(error)
        raise error

    sendEmail(data['recipient'], data['subject'], data['message'])


    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {
            "Access-Control-Allow-Origin" : "*"
        },
    }

def validateCaptcha(captchaResponse):

    print(os.environ.get('CAPTCHA_SECRET'))
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data = {
            'secret': os.environ.get('CAPTCHA_SECRET'),
            'response': captchaResponse,
        }
    )

    if not response.ok:
        raise Exception('Response error')

    data = response.json()

    print('Captcha Response', data)

    if not data['success']:
        raise Exception('Captcha validation error')

    return data['success']

def sendEmail(recipient, subject, body):

    sender=os.environ.get('SENDER')

    print("sending email [Recipient: {} ] [Sender: {} ]".format(recipient, sender))
    #Provide the contents of the email.
    response = sesClient.send_email(
        Destination={
            'ToAddresses': [
                sender,
            ],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': body,
            },
        },
        Source=sender,
        ReplyToAddresses=[
            recipient
        ]
    )
