import os
import re
import json
import boto3
import requests
import traceback

CHARSET = "UTF-8"

sesClient = boto3.client('ses',region_name=os.environ.get('AWS_SES_REGION'))

def lambda_handler(event, context):
    print("handling call [Event: {} ] [Context: {} ] ".format(event, context))

    response = {}
    statusCode = 200

    try:
        data = getContent(event['body'])
        validateCaptcha(data['g-recaptcha-response'])
        sendEmail(data['recipient'], data['subject'], data['message'])

    except AssertionError as error:
        response["message"] = "Validation error [ {} ]".format(error)
        statusCode = 400
        traceback.print_exc()

    except Exception as error:
        response["message"] = "Unhandled error"
        statusCode = 500
        traceback.print_exc()


    # TODO implement
    return {
        'statusCode': statusCode,
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
        raise AssertionError('Captcha validation error')

    return data['success']

def getContent(body):

    if body is None:
        raise AssertionError('Payload is empty')

    data = json.loads(body)

    print("data [ {} ]".format(data))

    expected_fields = ["g-recaptcha-response", "recipient", "message", "subject", "name"]

    for field in expected_fields:
        if not field in data:
            message = 'Missing required parameter [ {} ]'.format(field)
            print(message)
            raise AssertionError(message)

    return data


def sendEmail(recipient, subject, body):

    sender=os.environ.get('SENDER')

    print("sending email [Recipient: {} ] [Sender: {} ]".format(recipient, sender))


    message="Email from {} \n click reply to respond to email. \n\n {}".format(recipient, body)

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
                    'Data': message,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': subject,
            },
        },
        Source=sender,
        ReplyToAddresses=[
            recipient
        ]
    )
